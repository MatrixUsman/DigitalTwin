"""Independent compact architecture and explicit inference-artifact loading."""
import io
import numpy as np


def make_model(config, seed, compile_for_training=True):
    import tensorflow as tf
    tf.keras.utils.set_random_seed(seed)
    tf.config.experimental.enable_op_determinism()
    c = config["cnn"]
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(config["history"], len(config["columns"]))),
        tf.keras.layers.Conv1D(c["filters"], c["kernel_size"], activation=c["activation"], padding="valid"),
        tf.keras.layers.Conv1D(c["filters"], c["kernel_size"], activation=c["activation"], padding="valid"),
        tf.keras.layers.MaxPooling1D(c["pool_size"]),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(len(config["columns"]), kernel_initializer=c["dense_kernel_initializer"]),
        tf.keras.layers.Reshape((1, len(config["columns"]))),
    ])
    if compile_for_training:
        model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=c["learning_rate"]), loss="mse")
    return model


def weights_bytes(model):
    stream = io.BytesIO()
    np.savez(stream, **{f"w{i}": w for i, w in enumerate(model.get_weights())})
    return stream.getvalue()


def load_weights_artifact(config, path):
    model = make_model(config, seed=0, compile_for_training=False)
    reference = model.get_weights()
    with np.load(path, allow_pickle=False) as archive:
        if set(archive.files) != {f"w{i}" for i in range(len(reference))}:
            raise ValueError("Weight inventory mismatch")
        weights = [archive[f"w{i}"] for i in range(len(reference))]
    if any(w.shape != r.shape or w.dtype != r.dtype or not np.isfinite(w).all()
           for w, r in zip(weights, reference)):
        raise ValueError("Weight shape/dtype/finiteness mismatch")
    model.set_weights(weights)
    return model


def predict(model, values, endpoints, history, batch_size):
    from core import batches
    return np.concatenate([model(x, training=False).numpy()[:, 0, :]
                           for x, _ in batches(values, endpoints, history, batch_size)])
