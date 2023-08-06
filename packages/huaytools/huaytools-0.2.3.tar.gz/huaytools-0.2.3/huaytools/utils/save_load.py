"""
保存到各种类型的文件
"""
import huaytools
import pickle


def save_to_pickle(obj, fname):
    """
    保存到 pickle 文件

    Args:
        obj: 需要保存的对象
        fname(str): 文件名

    Returns:
        None

    """
    fname = huaytools.maybe_mkdirs(fname, is_file=True)
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)


def load_from_pickle(fname):
    """
    从 pickle 加载对象

    Args:
        fname(str): 文件名

    Returns:

    """
    with open(fname) as f:
        return pickle.load(f)
