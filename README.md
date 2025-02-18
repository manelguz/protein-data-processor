<div id="top"></div>

  <h3 align="center">Protein data processor</h3>

  <p align="center">
    This Application is aimed to process Protein Data Bank (PDB) files to extract key information for downstream biological analysis.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This Application is aimed to process Protein Data Bank (PDB) files to extract key information for downstream biological analysis. This repository is maintained mainly by Manel Guzmán Castellana

The main goal is to show a backend python3 application that loads the pdb datan and performce inference on a pytorch model. The backend is containerized in a docker for easy deployment


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Numpy](https://numpy.org/)
* [Docker](https://docker.com/) or [Conda](https://anaconda.org/)
* [PyTorch](https://pytorch.org/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

In order to make our project reproductible, we have make use of the python package manager conda for easy local test and a Dockerfile for test isolation and deployment

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/protein-data-processor.git
   ```
2. Install Anaconda Manager or Docker

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* conda
  ```sh
  conda env create -f environment.yml
  ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
### Usage with conda
  ```
    conda activate esmfold

    python3 src/pdb_chain_predictor.py inputs/1bey.pdb # Call the script to perfom chain infernce in you conda enviroment
  ```

### Usage with docker
  ```
    docker-compose up --build ## Or docker-compose up on succesive runs
    python3 src/call_pdb_api.py inputs/1bey.pdb # Call the script to perfom chain infernce throw post request to the already launched docker
    docker-compose down
  ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact


Manel Guzmán Castellana - manelguz7@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png