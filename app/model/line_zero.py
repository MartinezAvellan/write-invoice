class Field:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __set_name__(self, owner, nome):
        self.nome = nome

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.raw_data[self.initial: self.final]


class Base:
    def __init__(self, data):
        self.raw_data = data

    def __repr__(self):
        fields = []
        for name, obj in self.__class__.__dict__.items():
            if isinstance(obj, Field):
                fields.append((name, str(getattr(self, name)).strip()))
        return "\n".join(f"{field}:{str(content).strip()}" for field, content in fields)

    def __dict__(self):
        fields = {}
        for name, obj in self.__class__.__dict__.items():
            if isinstance(obj, Field):
                fields[name] = str(getattr(self, name)).strip()

        return fields


class InvoiceLineZero(Base):
    nome_cedente = Field(2, 102)
    cnpj_cedente = Field(262, 276)
    data_geracao = Field(210, 218)
    data_vencimento = Field(202, 210)

