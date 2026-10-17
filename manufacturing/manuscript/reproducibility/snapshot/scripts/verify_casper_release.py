#!/usr/bin/env python3
"""Rehash original CASPER bytes and inspect PCAPNG container/timestamp headers.

No packet payload, address, interface name, comment or protocol is decoded. Raw
payload bytes are read only for the full-file hash. Original receipts and files
are never rewritten. PCAPNG was identified from magic bytes, not the .pcap suffix.
"""
import collections
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import struct
import subprocess
import sys
import time

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "local/casper_release_audit"
MANIFEST = PROJECT / "datasets/manifests/casper_v3_integrity_recheck.json"
SPEC = "https://www.ietf.org/archive/id/draft-ietf-opsawg-pcapng-05.html"

def stamp():
    return datetime.now(timezone.utc).isoformat()

def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(8*1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def parse_options(data, endian):
    """Return option code/bytes internally; only clock values leave this routine."""
    items = []
    pos = 0
    while pos < len(data):
        assert pos + 4 <= len(data), "Truncated option header"
        code, size = struct.unpack_from(endian+"HH", data, pos)
        pos += 4
        assert pos + ((size+3)//4)*4 <= len(data), "Truncated option value"
        value = data[pos:pos+size]
        pos += ((size+3)//4)*4
        if code == 0:
            assert size == 0, "Invalid end-of-options"
            assert not any(data[pos:]), "Unexpected bytes after end-of-options"
            break
        items.append((code,value))
    return items

def clock_stats():
    return {"timestamped_packets":0,"first_ticks":None,"last_ticks":None,
            "minimum_ticks":None,"maximum_ticks":None,"duplicate_adjacent_steps":0,
            "backward_adjacent_steps":0,"largest_backward_step_ticks":0,
            "maximum_forward_step_ticks":0,
            "forward_gaps_greater_than_seconds":{"1":0,"10":0,"60":0}}

def add_time(stats, ticks, denominator):
    stats["timestamped_packets"] += 1
    if stats["first_ticks"] is None:
        stats["first_ticks"] = stats["minimum_ticks"] = stats["maximum_ticks"] = ticks
    else:
        delta = ticks-stats["last_ticks"]
        stats["duplicate_adjacent_steps"] += delta == 0
        stats["backward_adjacent_steps"] += delta < 0
        stats["largest_backward_step_ticks"] = max(stats["largest_backward_step_ticks"],-delta)
        stats["maximum_forward_step_ticks"] = max(stats["maximum_forward_step_ticks"],delta)
        for sec in stats["forward_gaps_greater_than_seconds"]:
            stats["forward_gaps_greater_than_seconds"][sec] += delta > int(sec)*denominator
        stats["minimum_ticks"] = min(stats["minimum_ticks"],ticks)
        stats["maximum_ticks"] = max(stats["maximum_ticks"],ticks)
    stats["last_ticks"] = ticks

def exact_epoch(ticks, interface):
    denominator = interface["timestamp_ticks_per_second"]
    seconds, fraction = divmod(ticks,denominator)
    seconds += interface["timestamp_offset_seconds"]
    return {"raw_ticks":ticks,"epoch_whole_seconds":seconds,
            "fraction_numerator":fraction,"fraction_denominator":denominator,
            "utc_whole_second_representation":datetime.fromtimestamp(seconds,timezone.utc).isoformat(),
            "interpretation":"Recorded epoch representation; accuracy, local timezone and clock synchronization are not established."}

def pcapng(path):
    h = hashlib.sha256()
    size = path.stat().st_size
    sections, counts = [],collections.Counter()
    consumed = 0
    packet_count = simple_count = payload_bytes = 0
    cap_truncated = cap_oversize = cap_zero = 0
    endian = None
    start = time.monotonic()
    with path.open("rb",buffering=8*1024*1024) as stream:
        def read(n):
            nonlocal consumed
            data = stream.read(n)
            h.update(data)
            consumed += len(data)
            assert len(data)==n, "Truncated block"
            return data
        while consumed < size:
            first = read(8)
            if first[:4] == b"\x0a\x0d\x0d\x0a":
                bom = read(4)
                assert bom in (b"\x4d\x3c\x2b\x1a",b"\x1a\x2b\x3c\x4d"), "Bad PCAPNG byte order magic"
                endian = "<" if bom==b"\x4d\x3c\x2b\x1a" else ">"
                length = struct.unpack(endian+"I",first[4:])[0]
                assert 28 <= length <= 64*1024*1024 and length%4==0
                assert consumed+length-12 <= size
                rest = read(length-12)
                assert struct.unpack_from(endian+"I",rest,len(rest)-4)[0]==length
                major,minor,section_length = struct.unpack_from(endian+"HHq",rest)
                assert (major,minor)==(1,0), "Only observed PCAPNG version 1.0 is supported"
                opts = parse_options(rest[12:-4],endian)
                sections.append({"section_index":len(sections),"byte_order":"little" if endian=="<" else "big",
                    "major":major,"minor":minor,"declared_section_length":section_length,
                    "option_codes_only":[c for c,v in opts],"interfaces":[],"timestamped_packet_blocks":0,"simple_packet_blocks":0})
                counts[str(0x0a0d0d0a)] += 1
                continue
            assert endian is not None and sections, "Missing PCAPNG section header"
            block_type,length = struct.unpack(endian+"II",first)
            assert 12<=length<=64*1024*1024 and length%4==0, "Invalid or excessive block length"
            assert consumed+length-8<=size,"Block exceeds file boundary"
            rest = read(length-8)
            assert struct.unpack_from(endian+"I",rest,len(rest)-4)[0]==length,"Block trailer length mismatch"
            body = memoryview(rest)[:-4]
            counts[str(block_type)] += 1
            section = sections[-1]
            if block_type == 1:
                assert len(body)>=8
                link_type,reserved,snaplen = struct.unpack_from(endian+"HHI",body)
                opts = parse_options(body[8:],endian)
                resolutions=[v for c,v in opts if c==9]
                offsets=[v for c,v in opts if c==14]
                assert len(resolutions)<=1 and len(offsets)<=1,"Repeated clock options"
                assert not resolutions or len(resolutions[0])==1
                assert not offsets or len(offsets[0])==8
                resolution = resolutions[0][0] if resolutions else 6
                base,exponent = (2,resolution&0x7f) if resolution&0x80 else (10,resolution)
                offset = struct.unpack(endian+"q",offsets[0])[0] if offsets else 0
                section["interfaces"].append({"interface_index":len(section["interfaces"]),
                    "link_type_numeric":link_type,"reserved":reserved,"snaplen":snaplen,
                    "option_codes_only":[c for c,v in opts],"timestamp_resolution_option_present":bool(resolutions),
                    "timestamp_resolution_base":base,"timestamp_resolution_exponent":exponent,
                    "timestamp_ticks_per_second":base**exponent,"timestamp_offset_option_present":bool(offsets),
                    "timestamp_offset_seconds":offset,"clock":clock_stats()})
            elif block_type in (2,6):
                assert len(body)>=20
                if block_type==6:
                    interface_id,high,low,caplen,original = struct.unpack_from(endian+"IIIII",body)
                else:
                    interface_id,drops,high,low,caplen,original = struct.unpack_from(endian+"HHIIII",body)
                assert interface_id<len(section["interfaces"]),"Unknown packet interface"
                interface = section["interfaces"][interface_id]
                padded=((caplen+3)//4)*4
                assert 20+padded<=len(body),"Captured length exceeds packet block"
                # Validate option framing after the opaque payload; values are not retained.
                parse_options(body[20+padded:],endian)
                assert interface["snaplen"]==0 or caplen<=interface["snaplen"],"Captured length exceeds snaplen"
                cap_truncated += caplen<original
                cap_oversize += caplen>original
                cap_zero += caplen==0
                payload_bytes += caplen
                packet_count += 1
                section["timestamped_packet_blocks"] += 1
                add_time(interface["clock"],(high<<32)|low,interface["timestamp_ticks_per_second"])
            elif block_type==3:
                assert section["interfaces"] and len(body)>=4
                original=struct.unpack_from(endian+"I",body)[0]
                snaplen=section["interfaces"][0]["snaplen"]
                captured=min(original,snaplen) if snaplen else original
                assert 4+((captured+3)//4)*4==len(body)
                payload_bytes += captured
                simple_count += 1
                packet_count += 1
                section["simple_packet_blocks"] += 1
            # Other blocks are hashed and framing-checked without interpreting content.
            if packet_count and packet_count%1000000==0:
                print(f"Packet-container headers: {packet_count}; {time.monotonic()-start:.1f}s",flush=True)
    assert consumed==size
    for section in sections:
        for interface in section["interfaces"]:
            clock=interface["clock"]
            if clock["timestamped_packets"]:
                clock["recorded_epoch_extrema"]={k:exact_epoch(clock[k],interface) for k in ("first_ticks","last_ticks","minimum_ticks","maximum_ticks")}
    return {"container":"PCAPNG","filename_suffix_is_not_container_proof":True,
        "sha256":h.hexdigest(),"bytes_consumed":consumed,"file_bytes":size,
        "block_counts_by_numeric_type":dict(counts),"sections":sections,
        "packet_blocks_total":packet_count,"packet_blocks_without_timestamp":simple_count,
        "captured_payload_bytes_hashed_not_decoded":payload_bytes,
        "captured_shorter_than_original_count":cap_truncated,
        "captured_longer_than_original_count":cap_oversize,"zero_captured_length_count":cap_zero,
        "framing_and_file_boundary_checks":"passed","elapsed_seconds":time.monotonic()-start,
        "limitations":["Precision/resolution does not establish timestamp accuracy or synchronized clocks.",
          "Only container headers, lengths and timing options were interpreted; packet protocols, endpoints, interface names and comments were not decoded.",
          "Clock comparisons are per interface within section, in file order; no cross-interface synchronization assumed.",
          "Nonpacket block contents are not semantically validated; CRC/packet checksum validation is outside this audit."]}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    receipt_path=PROJECT/"datasets/manifests/casper_v3_receipt.json"
    receipt_bytes=receipt_path.read_bytes()
    receipt=json.loads(receipt_bytes)
    record={"schema_version":1,"project":"manufacturing","audit_started_at_utc":stamp(),
        "command":"python3 manufacturing/scripts/verify_casper_release.py","working_directory":". (repository root)",
        "python":sys.version,"platform":platform.platform(),"script_sha256":hash_file(Path(__file__)),
        "original_receipt_sha256":hashlib.sha256(receipt_bytes).hexdigest(),"original_receipt_modified":False,
        "raw_files_modified":False,"model_or_network_replay_executed":False,
        "format_reference":{"url":SPEC,"status":"IETF Internet-Draft -05; format reference, not a published RFC"},"files":[]}
    entries=[{"local_path":receipt["archive"]["local_path"],"bytes":receipt["archive"]["bytes"],"sha256":receipt["archive"]["sha256"]}]+receipt["files"]
    for entry in entries:
        path=PROJECT/entry["local_path"]
        print("Checking "+path.name,flush=True)
        st=path.stat()
        ignored=subprocess.run(["git","check-ignore","-q",str(path)],cwd=PROJECT).returncode==0
        assert not path.is_symlink() and ignored
        assert st.st_size==entry["bytes"] and not st.st_mode&0o222
        if path.name=="arms.pcap":
            profile=pcapng(path)
            actual=profile["sha256"]
            profile_path=OUT/"pcapng_header_profile.json"
            profile_path.write_text(json.dumps(profile,indent=2)+"\n")
            record["capture_header_profile"]={"local_path":str(profile_path.relative_to(PROJECT)),"sha256":hash_file(profile_path),"bytes":profile_path.stat().st_size}
            record["capture_summary"]={k:profile[k] for k in ["container","filename_suffix_is_not_container_proof","packet_blocks_total","packet_blocks_without_timestamp","block_counts_by_numeric_type","framing_and_file_boundary_checks","captured_shorter_than_original_count","captured_longer_than_original_count","zero_captured_length_count"]}
        else:
            actual=hash_file(path)
        assert actual==entry["sha256"],"SHA-256 differs from acquisition receipt: "+path.name
        assert path.stat().st_size==st.st_size and path.stat().st_mtime_ns==st.st_mtime_ns
        record["files"].append({"local_path":entry["local_path"],"bytes":st.st_size,"sha256":actual,
            "original_receipt_match":True,"read_only_mode":True,"git_ignored":ignored,"symlink":False})
        print("SHA-256, bytes and storage checks passed: "+path.name,flush=True)
    assert receipt_path.read_bytes()==receipt_bytes
    record["audit_completed_at_utc"]=stamp()
    record["status"]="all_six_artifact_hashes_match_and_capture_container_headers_validated"
    record["limitations"]=["Byte identity is local receipt identity, not publisher-checksum or published-run correspondence.",
        "Capture metadata provides no proof of synchronization with controller or IMU clocks; detailed timestamps remain local.",
        "No ZIP re-extraction or second CRC pass was needed; original receipt records acquisition CRC validation."]
    MANIFEST.write_text(json.dumps(record,indent=2)+"\n")
    print("Fresh integrity and capture-header audit complete; no originals changed.",flush=True)

if __name__=="__main__":
    main()
