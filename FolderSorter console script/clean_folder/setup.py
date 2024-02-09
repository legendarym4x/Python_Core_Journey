from setuptools import setup

setup(name='clean_folder',
      version='0.0.1',
      description='Clean folder "Temp" from trash',
      url='https://github.com/legendarym4x',
      author='Maksim Nesterovskyi',
      author_email='maxwel842@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={
          'console_scripts': ['clean-folder = clean_folder.clean:main']

      },          
)