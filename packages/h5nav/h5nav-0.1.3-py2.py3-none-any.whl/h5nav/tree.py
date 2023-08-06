from collections import UserDict


class Leaf(object):
    """Container class for dataset or attribute"""
    def __init__(self, name, h5obj):
        self.name = name
        self.h5obj = h5obj

    @property
    def value(self):
        """hdf5 object value"""
        return self.h5obj[:]


class Group(UserDict):
    """Container class for groups"""
    def __init__(self, name, data):
        UserDict.__init__(self, data)
        self.name = name

    def _explore(self, grp_obj):
        """Split group contents in groups, datasets, attributes"""
        groups = [grp_obj[key] for key in grp_obj.keys()
                  if grp_obj[key].__class__.__name__ == "Group"]
        datasets = [grp_obj[key] for key in grp_obj.keys()
                    if grp_obj[key].__class__.__name__ == "Dataset"]
        attributes = [grp_obj[key] for key in grp_obj.keys()
                      if grp_obj[key].__class__.__name__ == "Attribute"]
        return groups, datasets, attributes

class Tree(object):
    """Agile tree representation of full hdf5 file"""
    def __init__(self, h5fh):
        self.root = Group(h5fh['/']



def parse_h5(h5fh):

        return [f for f in self.h5file[self.position].keys()
                if self.h5file[self.position + f].__class__.__name__
                   == "Dataset"]
