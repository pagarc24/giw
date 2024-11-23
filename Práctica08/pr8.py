"""
Asignatura: GIW
Práctica 8
Grupo: 07
Autores:    NICOLÁS JUAN FAJARDO CARRASCO
            PABLO GARCÍA FERNÁNDEZ
            MANUEL LOURO MENESES
            ROBERTO MORENO GUILLÉN

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

###
### <DEFINIR AQUÍ LAS CLASES DE MONGOENGINE>
###

from mongoengine import (
    Document, EmbeddedDocument, StringField, IntField, FloatField,
    DateField, ListField, EmbeddedDocumentField, ReferenceField,
    ValidationError
)
import re


def validate_field(value, field_name, expected_types):
    """Valida que un campo no sea None y que sea del tipo esperado."""
    if value is None:
        raise ValidationError(f"{field_name} no puede ser None.")
    if not isinstance(value, expected_types):
        expected = ", ".join(
            t.__name__ if isinstance(expected_types, tuple) else expected_types.__name__
            for t in (expected_types if isinstance(expected_types, tuple) else [expected_types])
        )
        raise ValidationError(f"{field_name} debe ser de tipo {expected}.")


class Tarjeta(Document):
    nombre = StringField(required=True, min_length=2)
    numero = StringField(required=True, regex=r'^\d{16}$')
    mes = StringField(required=True, regex=r'^\d{2}$')
    year = StringField(required=True, regex=r'^\d{2}$')
    cvv = StringField(required=True, regex=r'^\d{3}$')

    def clean(self):
        validate_field(self.nombre, "nombre", str)
        validate_field(self.numero, "numero", str)
        validate_field(self.mes, "mes", str)
        validate_field(self.year, "year", str)
        validate_field(self.cvv, "cvv", str)


class Producto(Document):
    codigo_barras = StringField(required=True, unique=True)
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True, min_value=0)
    categorias_secundarias = ListField(IntField(min_value=0))

    def clean(self):
        # Validar código de barras
        validate_field(self.codigo_barras, "codigo_barras", str)
        if not re.match(r'^\d{13}$', self.codigo_barras):
            raise ValidationError("El código de barras debe tener 13 dígitos.")
        suma = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(self.codigo_barras[:-1]))
        digito_control = (10 - suma % 10) % 10
        if int(self.codigo_barras[-1]) != digito_control:
            raise ValidationError("El código de barras EAN-13 no es válido.")

        # Validar categorías
        
        if not isinstance(self.categorias_secundarias, list):
            raise ValidationError("Las categorías secundarias deben ser una lista.")

        for categoria in self.categorias_secundarias:
            if not isinstance(categoria, int):
                raise ValidationError("Todas las categorías secundarias deben ser enteros positivos.")
       
        validate_field(self.categoria_principal, "categoria_principal", int)
        if self.categorias_secundarias:
            if self.categoria_principal not in self.categorias_secundarias:
                raise ValidationError("La categoría principal debe estar en las categorías secundarias.")
            if self.categorias_secundarias[0] != self.categoria_principal:
                raise ValidationError("La categoría principal debe ser la primera en las categorías secundarias.")


class Linea(EmbeddedDocument):
    num_items = IntField(required=True, min_value=1)
    precio_item = FloatField(required=True, min_value=0.01)
    nombre_item = StringField(required=True, min_length=2)
    total = FloatField(required=True, min_value=0.01)
    producto = ReferenceField(Producto, required=True)

    def clean(self):
        validate_field(self.num_items, "num_items", int)
        validate_field(self.precio_item, "precio_item", (int, float))
        validate_field(self.total, "total", (int, float))
        validate_field(self.nombre_item, "nombre_item", str)
        validate_field(self.producto, "producto", Producto)

        if self.total != self.num_items * self.precio_item:
            raise ValidationError("El total debe ser igual a num_items * precio_item.")
        if self.producto and not self.producto.pk:
            raise ValidationError("El producto debe estar guardado en la base de datos.")
        if self.nombre_item != self.producto.nombre:
            raise ValidationError("El nombre del producto debe coincidir con el de la línea.")


class Pedido(Document):
    total = FloatField(required=True, min_value=0.01)
    fecha = StringField(required=True, regex=r'^\d{4},\d{2},\d{2},\d{2},\d{2},\d{2},\d{6}$')
    lineas = ListField(EmbeddedDocumentField('Linea'), required=True)

    def clean(self):
        if not isinstance(self.lineas, list):
            raise ValidationError("Las líneas deben ser una lista.")
        suma_totales = sum(linea.total for linea in self.lineas if linea.total is not None)
        if self.total != suma_totales:
            raise ValidationError("El total del pedido no coincide con la suma de las líneas.")

        productos = [linea.producto for linea in self.lineas if linea.producto and linea.producto.pk]
        if len(productos) != len(set(productos)):
            raise ValidationError("No puede haber líneas con productos duplicados.")


class Usuario(Document):
    dni = StringField(required=True, unique=True)
    nombre = StringField(required=True, min_length=2)
    apellido1 = StringField(required=True, min_length=2)
    apellido2 = StringField()
    f_nac = DateField(required=True)
    tarjetas = ListField(ReferenceField(Tarjeta))
    pedidos = ListField(ReferenceField(Pedido))

    def clean(self):
        validate_field(self.dni, "dni", str)
        if not re.match(r'^\d{8}[A-Z]$', self.dni):
            raise ValidationError("El DNI debe tener 8 dígitos seguidos de una letra.")
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(self.dni[:-1])
        letra = self.dni[-1]
        if letras[numero % 23] != letra:
            raise ValidationError("La letra del DNI no es correcta.")
        
        # Validar tarjetas directamente desde _data para evitar resolución automática
        tarjetas = self._data.get("tarjetas", None)
        if tarjetas is not None:
            if not isinstance(tarjetas, list):
                raise ValidationError("El campo tarjetas debe ser una lista.")
            for tarjeta in tarjetas:
                if not isinstance(tarjeta, Tarjeta):
                    raise ValidationError("Todos los elementos de tarjetas deben ser instancias de Tarjeta.")
                if not tarjeta.pk:
                    raise ValidationError("Todas las tarjetas referenciadas deben estar guardadas en la base de datos.")


