from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout as Box
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton
from kivy.uix.gridlayout import GridLayout
import database
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from functools import partial
from kivy.core.window import Window
from kivy.core.text import LabelBase


class ProductoItem(OneLineAvatarIconListItem):

    nombre = StringProperty("")
    precio = NumericProperty(0)
    cantidad = NumericProperty(0)
    index = NumericProperty(0)

class EditarProducto(Box):

    nombre = StringProperty("")
    precio = NumericProperty(0)
    cantidad = NumericProperty(0)

class MainApp(MDBoxLayout):

    productos = ListProperty()
    total = NumericProperty(0)
    dialog = None
    producto_actual = None

    LabelBase.register(name="Roboto_Mono_titulo", fn_regular="fuentes/RobotoMono-Bold.ttf")
    LabelBase.register(name="Roboto_Mono_contenido", fn_regular="fuentes/RobotoMono-SemiBoldItalic.ttf")
    LabelBase.register(name="Ancizar_botones", fn_regular="fuentes/AncizarSans-Bold.ttf")
    LabelBase.register(name="Ancizar_contenido", fn_regular="fuentes/AncizarSans-MediumItalic.ttf")


    def crear_caja_emergente (self, titulo, texto) : 

        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        message = Label(
        text = texto,
        font_name = "Roboto_Mono_contenido",
        font_size = '15sp',
        color = '#FFFFFF',
        halign = 'center',
        valign = 'middle'
        )

        message.bind(size=message.setter('text_size'))

        boton_cerrar = Button(
            text = "Cerrar",
            font_name = "Ancizar_botones",
            size_hint_y = None,
            height = 30,
            background_color = '#00C853',
            color = '#FFFFFF',  
            bold = True
        )

        content.add_widget(message)
        content.add_widget(boton_cerrar)

        popup = Popup(
            title = titulo, 
            title_size = 20, 
            title_align = 'center',
            title_color = (1, 1, 1, 1),
            title_font = "Roboto_Mono_titulo",
            background_color = '#1f1f1f',
            separator_color = '#00C853',
            size_hint=(0.8, 0.4),
            content = content,
            auto_dismiss = False,
        )

        boton_cerrar.bind(on_release=popup.dismiss)
        popup.open()


    def mostrar_dia_de_la_semana(self) : 

        dias_semana = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo"
        }

        return dias_semana

    
    def mostrar_nombre_de_meses (self) : 

        meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }

        return meses

    
    def mostrar_fecha_actual_estilizada (self) : 

        fecha = datetime.now().strftime("%d-%m-%Y")
        return fecha
    

    def guardar_ganancia(self):
        
        nombre_del_dia = self.mostrar_dia_de_la_semana()
        numero_del_dia = datetime.now().weekday()
        fecha = self.mostrar_fecha_actual_estilizada()

        fecha_con_dia = f"{nombre_del_dia[numero_del_dia]} {fecha}"
        total_productos= len(self.productos)

        numero_del_mes = datetime.now().month
        mes = self.mostrar_nombre_de_meses()
        anio = datetime.now().year

        try: 
                
            for indice in range(total_productos) :

                total_tiempo_real = self.productos[indice]["precio"] * self.productos[indice]["cantidad"]
                datos = database.datos_guardados(self.productos[indice]["nombre"], 
                                                self.productos[indice]["precio"],
                                                self.productos[indice]["cantidad"],
                                                fecha_con_dia,
                                                total_tiempo_real,
                                                mes[numero_del_mes],
                                                anio
                                                )    

                datos.guardar_en_base_datos()
                
            self.crear_caja_emergente("Mensaje", "Ganancia guardada en la base de datos.")
        
        except Exception as error: 
                
                self.crear_caja_emergente("Error", "No se pudo guardar la ganancia en la base de datos.")
                print(error)


    def mostrar_historial (self, *args) : 

        try:

            numero_del_mes = datetime.now().month
            mes = self.mostrar_nombre_de_meses()
            anio = datetime.now().year

            # Obtener datos de la base de datos
            base_de_datos = database.datos_guardados("", 0, 0, "", 0, "", 0)
            datos = base_de_datos.seleccionar_meses_y_anio(mes[numero_del_mes], anio)

            # Crear MDList con datos
            lista = MDList()
            for item in datos:
                texto = f"{item[0]} {item[1]}"
                valor = OneLineListItem(text=texto)
                valor.bind(on_release=partial(self.mostrar_todos_los_dias, titulo = texto))
                lista.add_widget(valor)  # ✅ Ahora sí agregas el que tiene el evento


            # ScrollView que contiene la lista
            scroll = MDScrollView()
            scroll.size_hint = (1, None)
            scroll.height = 300  # Altura fija para que no se solape con el título
            scroll.add_widget(lista)

            # Crear/actualizar el diálogo
            if self.dialog:
                self.dialog.dismiss()

            self.pantalla_alto = Window.height
            dialog_height = self.pantalla_alto * 0.8

            self.dialog = MDDialog(
                title="Historial de Ventas",
                type="custom",
                content_cls=scroll,
                buttons=[
                    MDRaisedButton(text="Cerrar", on_release=lambda x: self.dialog.dismiss(), 
                                font_name = "Ancizar_botones", font_size = "16sp")
                ],
                size_hint=(0.9, None),
                height = dialog_height,
            )

            self.dialog.open()
        
        except Exception as error:

            self.crear_caja_emergente("Advertencia", "No hay historial de ventas o hubo un error en la muestra\n\nPor favor intente de nuevo.")
            print(error)


    def mostrar_todos_los_dias(self, instance, titulo):

        numero_del_mes = datetime.now().month
        mes = self.mostrar_nombre_de_meses()

        base_de_datos = database.datos_guardados("", 0, 0, "", 0, "", 0)
        datos = base_de_datos.seleccionar_fecha_y_su_total(mes[numero_del_mes])

        self.dialog.content_cls.clear_widgets()  
        self.dialog.title = f"Recaudación de {titulo}"
        
        lista = MDList()

        for item in datos:
            texto = f"Fecha = {item[0]}"
            valor = OneLineListItem(text=texto)
            valor.bind(on_release=partial(self.mostrar_productos_por_fecha,  titulo_fecha = item[0]))
            lista.add_widget(valor) 

        scroll = MDScrollView()
        scroll.size_hint = (0.9, None)
        scroll.height = self.pantalla_alto * 0.6
        scroll.width = self.dialog.width

        scroll.add_widget(lista)

        self.dialog.content_cls.add_widget(scroll) 

        
    def mostrar_productos_por_fecha (self, instance, titulo_fecha) : 

        base_de_datos = database.datos_guardados("", 0, 0, "", 0, "", 0)
        datos = base_de_datos.abrir_detalles_de_la_fecha(titulo_fecha)

        total_precio = base_de_datos.abrir_total_precio_de_fecha(titulo_fecha)
        total_cantidad = base_de_datos.abrir_total_cantidad_de_fecha(titulo_fecha)

        self.dialog.dismiss()
        
        self.grid = GridLayout(cols=4, spacing=10, padding=10)
        self.grid.bind(minimum_height=self.grid.setter("height"))

        encabezados = ["Producto", "Cantidad", "Precio", "Total"]
        for subtitulo in encabezados:
            self.grid.add_widget(MDLabel(text=f"[b]{subtitulo}[/b]", markup=True, font_name="Ancizar_contenido"))

        for item in datos:
            self.grid.add_widget(MDLabel(text=item[0], font_name="Ancizar_contenido"))
            self.grid.add_widget(MDLabel(text=f"{item[1]}", font_name="Ancizar_contenido"))
            self.grid.add_widget(MDLabel(text=f"${item[2]}", font_name="Ancizar_contenido"))
            self.grid.add_widget(MDLabel(text=f"${item[3]}", font_name="Ancizar_contenido"))

        # Líneas separadoras y totales
        for _ in range(4):
            self.grid.add_widget(MDLabel(text="_______"))

        for _ in range(4):
            self.grid.add_widget(MDLabel(text=""))

        self.grid.add_widget(MDLabel(text="Total Vendido", bold=True, font_name="Ancizar_contenido"))
        self.grid.add_widget(MDLabel(text=f"${total_precio[0][0]}", bold=True, font_name="Ancizar_contenido"))

        for _ in range(2):
            self.grid.add_widget(MDLabel(text=""))

        self.grid.add_widget(MDLabel(text="Total Cantidad", bold=True, font_name="Ancizar_contenido"))
        self.grid.add_widget(MDLabel(text=f"{total_cantidad[0][0]}", bold=True, font_name="Ancizar_contenido"))

        popup = Popup (

            title = f"Recaudación del {titulo_fecha}", 
            title_font = "Roboto_Mono_titulo",
            title_size = "18sp",
            content = self.grid,
            size_hint = (0.9, 0.7), 
            size = (500, 350),
            background_color = '#1f1f1f',
            separator_color = '#00C853',
            auto_dismiss=True,
        )

        popup.open()


    def agregar_producto(self):
        self.productos.append({"nombre": "Nuevo producto", "precio": 0, "cantidad": 0})
        self.actualizar_total()

    def eliminar_producto(self, index):
        del self.productos[index]
        self.actualizar_total()

    def aumentar_cantidad(self, index):
        self.productos[index]["cantidad"] += 1
        self.actualizar_total()

    def disminuir_cantidad(self, index):
        if self.productos[index]["cantidad"] > 0:
            self.productos[index]["cantidad"] -= 1
            self.actualizar_total()

    def editar_producto(self, index):
        self.producto_actual = index
        producto = self.productos[index]

        self.dialog = MDDialog(
            title = "Editar Producto",
            type = "custom",
            content_cls=EditarProducto(
                nombre="",
                precio=producto['precio'],
                cantidad=producto['cantidad']
            ),
            buttons=[
                MDFlatButton(text="CANCELAR", font_name = "Ancizar_botones", font_size = "16sp" , on_release=self.cerrar_dialogo),
                MDFlatButton(text="GUARDAR", font_name = "Ancizar_botones", font_size = "16sp" , on_release=self.guardar_cambios)
            ],
        )
        self.dialog.open()


    def guardar_cambios(self, *args):
        datos = self.dialog.content_cls
        self.productos[self.producto_actual]["nombre"] = datos.ids.nombre.text
        self.productos[self.producto_actual]["precio"] = float(datos.ids.precio.text)
        self.productos[self.producto_actual]["cantidad"] = int(datos.ids.cantidad.text)
        self.actualizar_total()
        self.dialog.dismiss()


    def cerrar_dialogo(self, *args):
        self.dialog.dismiss()


    def actualizar_total(self):
        self.total = sum(p["precio"] * p["cantidad"] for p in self.productos)

        productos_layout = self.ids.productos_layout
        productos_layout.clear_widgets()
        espacio_vacio ="           "

        for indice, producto in enumerate(self.productos):
            item = ProductoItem(
                text= espacio_vacio + f"{producto['nombre']} - ${producto['precio']:.2f} x {producto['cantidad']}",
                nombre=producto["nombre"],
                precio=producto["precio"],
                cantidad=producto["cantidad"],
                index=indice
            )
            #icon = IconRightWidget(icon="cart")
            #item.add_widget(icon)
            productos_layout.add_widget(item)

class NegocioApp(MDApp):
    icon = 'img\logo.png'
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"  # También puedes usar "Dark"
        return MainApp()

if __name__ == "__main__":
    NegocioApp().run()