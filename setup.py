from setuptools import setup, find_packages

setup(name='iapismdp',
      version='0.1.0',
      description='Implementation of stochastic service composition.',
      license='MIT',
      packages=find_packages(include=['iapismdp*']),
      zip_safe=False,
      install_requires=[
            "numpy",
            "graphviz",
            "websockets",
            "paho-mqtt",
            "requests",
            "logaut",
            "pythomata",
            "networkx",
            "pydotplus",
            "datetime",
            "mdp_dp_rl @ git+https://github.com/luusi/mdp-dp-rl.git#egg=mdp_dp_rl"
      ]
)
