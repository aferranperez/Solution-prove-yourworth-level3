import requests
import logging
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw


# Download the payload. Sign it with your name.
# Upload the modified image, your code, and your resum�.
# Do it all with code. Curl, Snoopy, Pear, Sockets... all good. Good luck.


class Test:
    _base_url_ = "https://www.proveyourworth.net/level3"
    _activate_url_ = "https://www.proveyourworth.net/level3/activate?statefulhash"
    _session_id_ = None
    _token_ = None
    _response_ = requests.Session()

    def __init__(self, name:str, email:str, cv:str):
        """Constructor"""
        self.name = name
        self.email = email
        self.cv = cv

    def get_session_id(self):
        request = self._response_.get(self._base_url_)
        self._session_id_ = request.cookies['PHPSESSID']
        logging.info(f"Get SESSION_ID: {self._session_id_}")

    def get_token(self):
        request = self._response_.get(self._base_url_)
        code_soup = BeautifulSoup(request.text,'html.parser')
        self._token_ = code_soup.find('input', {'name':'statefulhash'})['value']
        logging.info(f"Get TOKEN: {self._token_}") 

    def activate_account(self):
        request = self._response_.get(
            f'{self._activate_url_}={self._token_}'
        )
        logging.info(f'Activated account.')

    def get_image(self):
        request = self._response_.get(
            f'{self._base_url_}/payload',
            stream=True
        )
        image = request.raw
        logging.info("Downloaded image.")
        return image

    def sing_image(self):
        image  = Image.open(self.get_image())
        logging.info("Editing the image...")
        draw = ImageDraw.Draw(image)
        draw.text(
            (30, 60),
            f"{self.name}\nHash:{self._token_}\nEmail:{self.email}\nPython Developer and System Admin",
            fill=(255,0,0)
        )
        image.save("image_test.png", "PNG")
        logging.info("Saved sing image")

    def upload_data(self):
        payload = self._response_.get(
            f'{self._base_url_}/payload',
        )

        url = payload.headers['X-Post-Back-To']

        files = {
            "code" : open("main.py", "rb"),
            "resume" : open("cv.pdf", "rb"),
            "image" : open("image_test.png", "rb")
        }

        data = {
            "email" : self.email,
            "name" : self.name,
            "aboutme" : """
                        Software developer with a Telecommunication and Electronics engineering degree.
                        Proficiency in programming languages as Python, Javascript, C/C++ and others.
                        Network Manager and Web Developer with two years of experience.
                        Work with agile software development methodologies such as SCRUM and Kanban.
                        Involved in developing my skills as a programmer and open to learn new technologies.
                        Interested to join agile teams, where I can learn from my partners and contribute to its growth.
            """
        }

        request = self._response_.post(
            url,
            files=files,
            data=data
        )

        map(lambda x: x.close(), files)

        #Saving the request to inspect 
        with open("out.txt", "w") as sfile:
            sfile.write(request.text)


    def main(self):
        self.get_session_id()
        self.get_token()
        self.activate_account()
        self.sing_image()
        self.upload_data()
        

if __name__ == "__main__":
    logging.basicConfig(level= logging.INFO)

    name = "Alejandro Joel Ferran Perez"
    email = "aferranperez@gmail.com" 
    test = Test(name, email,"cv.pdf")

    try:
        test.main()

    except Exception as err:

        logging.warning("Ocurrio un error en el programa.")
        logging.warning(err)
    else:

        logging.info("El programa ha finalizado satisfactoriamente.")