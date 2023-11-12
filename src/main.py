from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship,  declarative_base, sessionmaker

Base = declarative_base()

class WebPage(Base):
    __tablename__ = 'webpage'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    elements = relationship('Elements', back_populates='webpage')


class Elements(Base):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    alt = Column(String)
    href = Column(String)
    value = Column(String)
    webpage_id = Column(Integer, ForeignKey('webpage.id'))
    webpage = relationship('WebPage', back_populates='elements')


# URL of the website to check
urls = ['https://www.mefos.unios.hr/index.php/hr/',
        'https://www.biologija.unios.hr/',
        'https://www.kemija.unios.hr/',
        'https://www.pravos.unios.hr/',
        'http://www.uaos.unios.hr/',
        'http://www.efos.unios.hr/',
        'https://www.ferit.unios.hr/',
        'https://www.fdmz.hr/index.php/hr/',
        'https://www.foozos.hr/',
        'https://www.ffos.unios.hr/'
        ]

# Element and class to search for
elements_to_find = ['h1',
                    'h2',
                    'h3',
                    'button',
                    'head',
                    'meta',
                    'img',
                    'header',
                    'nav',
                    'main',
                    'section',
                    'footer',
                    'a'
                    ]

engine = create_engine('postgresql://postgres:admin1234@localhost/postgres')

Session = sessionmaker(bind=engine)
session = Session()


Base.metadata.create_all(engine)

# Send an HTTP GET request
for ur in urls:
    response = requests.get(ur)
    newPage = WebPage(url=ur)
    if response.status_code == 200:

        # Define a mapping of element names to their corresponding classes and attributes
        element_mapping = {
            'img': {'class': 'Elements', 'alt_attr': 'alt'},
            'h1': {'class': 'Elements'},
            'h2': {'class': 'Elements'},
            'h3': {'class': 'Elements'},
            'header': {'class': 'Elements'},
            'nav': {'class': 'Elements'},
            'main': {'class': 'Elements'},
            'section': {'class': 'Elements'},
            'footer': {'class': 'Elements'},
            'button': {'class': 'Elements'},
            'a': {'class': 'Elements', 'href_attr': 'href'},
            'meta': {'class': 'Elements', 'name_attr': 'name'}
        }

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with the specified class
        page_elements = soup.find_all(elements_to_find)

        for el in page_elements:
            element_name = el.name
            element_info = element_mapping.get(element_name)

            if element_info:
                element_class = element_info['class']
                new_element = Elements(name=element_name)

                if 'alt_attr' in element_info and 'alt' in el.attrs:
                    new_element.alt = el['alt']

                if 'href_attr' in element_info and 'href' in el.attrs:
                    new_element.href = el['href']

                if 'name_attr' in element_info and 'name' in el.attrs:
                    new_element.value = el['name']

                newPage.elements.append(new_element)

        session.add(newPage)
        session.commit()

    else:
        print("Failed to retrieve the Webpage")

    print("Retrieved data from", ur)

session.close()