# dl-trainer-framework
This is an open resource repo for dl training framework.
- supervised-learning training
- multi-processing dataloader
- single-gpu

## Usage
### Requirements
- python3.*
- tensorflow == 1.14.0

### Run
- put your train & valid data in target directories in ***/data/****, and change the config path in ***/learner/config/config.py*** of `line 26` to `line 29`.
- run scripts in ***/op***

```shell
    sh op/run.sh | show.sh | stop.sh
```

## License
The repo is Open Resource Software released under the License. It is developed by [Chadyang](https://nnuyi.github.io/).
