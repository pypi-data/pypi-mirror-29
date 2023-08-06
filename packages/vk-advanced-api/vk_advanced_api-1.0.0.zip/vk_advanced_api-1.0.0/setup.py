from distutils.core import setup
import vk_advanced_api

setup(
    name='vk_advanced_api',
    version=vk_advanced_api.vkapi.__version__,
    packages=['vk_advanced_api'],
    install_requires=['requests', 'captcha_solver', 'lxml', 'parsel', 'pymitter'],
    url='https://github.com/Ar4ikov/vk_advanced_api',
    license='MIT License',
    author='Nikita Archikov',
    author_email='bizy18588@gmail.com',
    description='A simple MAV API wrapper for python (3.5 or newer)',
    keywords='mavapi, mav, api, wrappper, rugaming'

)
