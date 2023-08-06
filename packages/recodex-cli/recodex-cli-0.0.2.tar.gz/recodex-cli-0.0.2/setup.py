from setuptools import setup

setup(name='recodex-cli',
      version='0.0.2',
      description='ReCodEx CLI',
      long_description='A command line frontend to the ReCodEx programmer evaluation system',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Operating System :: Unix',
          'Programming Language :: Python :: Implementation :: CPython',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='recodex',
      url='https://github.com/ReCodEx/cli',
      author='ReCodEx team',
      license='MIT',
      packages=['recodex',
                ],
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=['click', 'requests', 'appdirs', 'ruamel.yaml', 'bs4', 'lxml', 'html2text'],
      entry_points={
          'console_scripts':
              ['recodex = recodex.cli:cli'],
          'recodex': [
              'codex = recodex.plugins.codex.cli:cli',
              'exercises = recodex.plugins.exercises.cli:cli',
              'caslogin = recodex.plugins.caslogin.cli:caslogin',
              'login = recodex.plugins.login.cli:login'
          ]
      }
)
