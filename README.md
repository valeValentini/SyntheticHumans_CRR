<br/>
<p align="center">
  <h3 align="center">Automatic Workflow Optimization for Photorealistic Synthetic Humans Creation
</h3>

</p>

![Downloads](https://img.shields.io/github/downloads/valeValentini/SyntheticHumans_CRR_PoliTo/total) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

![Screen Shot](images/screenshot.png)

The primary goal was to develop and implement an advanced workflow for Synthetic Human generation, with a focus on minimizing human intervention and ensuring an efficient, flexible process. 
This project aimed to transform RAI’s vast archive of images and videos resources into a valuable asset for creating photorealistic 3D avatars of significant personalities, such as historical figures or past celebrities.

#Automated 3D Head Reconstruction 
This was achieved through the Orchestrator, developed in partnership with PluxBox for the IBC2023 Accelerator Project. The Orchestrator is a sophisticated technological tool that integrates various stages - from image selection to super-resolution, culminating in three-dimensional face reconstruction. Automation in Face Reconstruction was facilitated by a script provided to the Orchestrator via Rest APIs, employing Blender FaceBuilder plugin's functionalities to create 3D face meshes from 2D images.

#Face Texture Reconstruction
The project also emphasized improving textures using Stable Diffusion and Artificial Intelligence to generate images of the reference subject. AI-generated images were found to be more suitable for texture production than traditional methods. This phase benefited from the refinement of LoRA training models, enabling the creation of realistic, detailed images crucial for generating uniform textures in Synthetic Human creation.

## Built With

Major Frameworks Utilized in the Project:

Through the Stable Diffusion Web UI provided by Automatic1111 it is possible to download and run Stable Diffusion locally. 

The Low-Rank Adaptation training was conducted using the Kohya Trainer, available on Google Colab. 
Approximately 80 images of the chosen subject were used for the training, usefull info can be found in this video.
After training the LoRA models using the Kohya Trainer, the resulting TensorFlow files of the subject were directly integrated into the local installation of the Stable Diffusion Web UI in the "stable-diffusion-webui/models/Lora" directory, enabling the usage of these custom-trained models in the SD WebUI.

The Realistic Vision V5.1 model is specifically designed and optimized for generating high-resolution, photorealistic images. This model is a critical component in achieving high-quality, results, and it functions within the stable diffusion framework, once downloaded, the model file needs to be placed in the "models/Stable-diffusion" directory the local installation of the Stable Diffusion Web UI.
Once the Web UI recognizes the new model, you can select it from the Stable Diffusion checkpoint input field. This step is crucial as it tells the system which specific model to use for generating images.

* [Automatic1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
* [LoRA Model Training](https://colab.research.google.com/github/Linaqruf/kohya-trainer/blob/main/kohya-LoRA-dreambooth.ipynb#scrollTo=p_SHtbFwHVl1)
* [Realistic Vision V5.1 Checkpoint](https://civitai.com/models/4201/realistic-vision-v51)

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* npm

```sh
npm install npm@latest -g
```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)

2. Clone the repo

```sh
git clone https://github.com/your_username_/Project-Name.git
```

3. Install NPM packages

```sh
npm install
```

4. Enter your API in `config.js`

```JS
const API_KEY = 'ENTER YOUR API';
```

## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

## Roadmap

See the [open issues](https://github.com/valeValentini/SyntheticHumans_CRR_PoliTo/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/valeValentini/SyntheticHumans_CRR_PoliTo/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/valeValentini/SyntheticHumans_CRR_PoliTo/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/valeValentini/SyntheticHumans_CRR_PoliTo/blob/main/LICENSE.md) for more information.

## Authors

* **Shaan Khan** - *Comp Sci Student* - [Shaan Khan](https://github.com/ShaanCoding/) - *Built ReadME Template*

## Acknowledgements

* [ShaanCoding](https://github.com/ShaanCoding/)
* [Othneil Drew](https://github.com/othneildrew/Best-README-Template)
* [ImgShields](https://shields.io/)
