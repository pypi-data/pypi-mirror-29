from datetime import datetime
import uuid
import copy


class Serializer():

    def dump(self, origin_instance):
        return self.typping(origin_instance)

    def cycling(self, instance):

        if isinstance(instance, (set, list)):
            m_list = []
            for item in instance:
                value = self.typping(item)
                m_list.append(value)
            return m_list
        if isinstance(instance, dict):
            m_dict = {}
            for item in instance:
                value = self.typping(instance[item])
                m_dict.update({item: value})
            return m_dict

    def typping(self, instance):

        if isinstance(instance, set):
            return self.cycling(instance)
        elif isinstance(instance, list):
            return self.cycling(instance)
        elif isinstance(instance, dict):
            return self.cycling(instance)
        elif isinstance(instance, (float, int, str, bytes, bool)):
            return instance
        elif isinstance(instance, uuid.UUID):
            return str(instance)
        elif isinstance(instance, datetime):
            return str(instance)
        elif instance is None:
            return None
        else:
            return self.typping(self.mapping(instance))

    def mapping(self, instance):
        if '__tablename__' in dir(instance):
            # a hack for sqlalchemy object
            return self.get_attr_dict_from_sqlalchemy_object(instance)
        else:
            return self.get_attr_dict(instance)

    def get_attr_dict_from_sqlalchemy_object(self, instance):
        full = {}
        for key in instance.__mapper__.c.keys():
            if not key.startswith('_') and key not in instance.exclude:
                full.update({key: getattr(instance, key)})
        return full

    def get_attr_dict(self, instance):

        full = dict([[e, getattr(instance, e)] for e in dir(instance)
                     if not e.startswith('_') and not hasattr(
                         getattr(instance, e), '__call__') and e not in self.exclude])
        propery = dict([[p, getattr(instance, e).__get__(instance, type(instance))]
                        for p in full if hasattr(full[p], 'fset')])
        full.update(propery)
        return full

serializer = Serializer()
