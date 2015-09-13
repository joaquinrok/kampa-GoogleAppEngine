"""Hello World API implemented using Google Cloud Endpoints.

Contains declarations of endpoint, endpoint methods,
as well as the ProtoRPC message class and container required
for endpoint method definition.
"""
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

# Datastore
from google.appengine.ext import db
# PIL
from PIL import Image, ImageFont, ImageDraw
import cStringIO

# If the request contains path or querystring arguments,
# you cannot use a simple Message class.
# Instead, you must use a ResourceContainer class
REQUEST_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    name=messages.StringField(1),
)

REQUEST_GREETING_CONTAINER = endpoints.ResourceContainer(
    period=messages.StringField(1),
    name=messages.StringField(2),
)

#//////////////

# ================================
#           Data Model
# ================================
class Data(db.Model):
    rec = db.FloatProperty(required=True)
    obj = db.FloatProperty(required=True)


# Store initial values
d = Data(rec=float(0),
         obj=float(0), key_name='mainData')
d.put()


# ================================
#         Request types
# ================================
REQUEST_ADD_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    addValue=messages.FloatField(1),
)

REQUEST_MODIFY_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    newValue=messages.FloatField(1),
)

# ================================
#         Response types
# ================================
class UpdateResponse(messages.Message):
    """String that stores a message."""
    recaudado = messages.StringField(1)
    objetivo = messages.StringField(2)


class ImageResponse(messages.Message):
    imgHTML = messages.StringField(1)

#/////////////

package = 'Hello'


class Hello(messages.Message):
    """String that stores a message."""
    greeting = messages.StringField(1)


@endpoints.api(name='helloworldendpoints', version='v1')
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    @endpoints.method(message_types.VoidMessage, Hello,
      path = "sayHello", http_method='GET', name = "sayHello")
    def say_hello(self, request):
      return Hello(greeting="Hello World")

    @endpoints.method(REQUEST_CONTAINER, Hello,
      path = "sayHelloByName", http_method='GET', name = "sayHelloByName")
    def say_hello_by_name(self, request):
      greet = "Hello {}".format(request.name)
      return Hello(greeting=greet)

    @endpoints.method(REQUEST_GREETING_CONTAINER, Hello,
      path = "greetByPeriod", http_method='GET', name = "greetByPeriod")
    def greet_by_period(self, request):
      greet = "Good {} {}".format(request.period, request.name)
      return Hello(greeting=greet)







    # ---------------------------
    # ADD AMOUNT
    @endpoints.method(REQUEST_ADD_CONTAINER, UpdateResponse,
                      path="addAmount", http_method='GET', name="addAmount")
    def add_amount(self, request):
        dd = db.Key.from_path('Data', 'mainData')
        main_data_entity = db.get(dd)

        rec = float(main_data_entity.rec)
        rec += float(request.addValue)

        main_data_entity.rec = rec
        main_data_entity.put()

        return self.get_values(message_types.VoidMessage())

    # ---------------------------
    # GET VALUES
    @endpoints.method(message_types.VoidMessage, UpdateResponse,
                      path="getValues", http_method='GET', name="getValues")
    def get_values(self, request):
        dd = db.Key.from_path('Data', 'mainData')
        dd_ret = db.get(dd)
        rec = float(dd_ret.rec)
        obj = float(dd_ret.obj)

        return UpdateResponse(recaudado=str(rec), objetivo=str(obj))

    # ---------------------------
    # CHANGE TOTAL
    @endpoints.method(REQUEST_MODIFY_CONTAINER, UpdateResponse,
                      path="changeTotal", http_method='GET', name="changeTotal")
    def change_tot(self, request):
        dd = db.Key.from_path('Data', 'mainData')
        main_data_entity = db.get(dd)

        rec = request.newValue

        main_data_entity.rec = rec
        main_data_entity.put()

        return self.get_values(message_types.VoidMessage())

    # ---------------------------
    # CHANGE OBJECTIVE
    @endpoints.method(REQUEST_MODIFY_CONTAINER, UpdateResponse,
                      path="changeObj", http_method='GET', name="changeObj")
    def change_obj(self, request):
        dd = db.Key.from_path('Data', 'mainData')
        main_data_entity = db.get(dd)

        obj = request.newValue

        main_data_entity.obj = obj
        main_data_entity.put()

        return self.get_values(message_types.VoidMessage())


    # ---------------------------
    # GENERATE IMAGE
    @endpoints.method(message_types.VoidMessage, ImageResponse,
                      path="generateImage", http_method='GET', name="generateImage")
    def gen_image(self, request):
        # Load cover background
        img = Image.open("res/cover.jpg")
        draw = ImageDraw.Draw(img)

        # Get number values from db
        dd = db.Key.from_path('Data', 'mainData')
        dd_ret = db.get(dd)
        rec = float(dd_ret.rec)
        obj = float(dd_ret.obj)
        num = int(obj - rec)

        # Draw numbers
        color = (62, 62, 62)
        font = ImageFont.truetype("res/SourceSansPro-Bold.ttf", 125)
        ini = 213
        y = 22
        sep = 106
        num_str = str(num)
        len_num = len(num_str)
        num_str = (" "*(5-len_num)) + num_str
        #if num <= 0:
        #    num_str = "kmpa!"
        for x in range(5):
            draw.text((ini+(sep*x), y), num_str[x], color, font)

        f = cStringIO.StringIO()
        # Save the image in the sting buffer (instead of in a file)
        img.save(f, "JPEG", quality=90)
        # Get the string buffer content
        content = f.getvalue()
        f.close()
        # Base64 encode for data URI scheme
        data_uri = content.encode("base64").replace("\n", "")
        # Show the image according to data URI scheme
        img_html = '<img id="theimage" style="margin-left:50px" src="data:image/jpeg;base64,%s" />' % data_uri

        return ImageResponse(imgHTML=img_html)


APPLICATION = endpoints.api_server([HelloWorldApi])
