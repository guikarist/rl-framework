from pathlib import Path
from typing import Any

from core import Model
from abc import ABC, abstractmethod


class TFKerasModel(Model, ABC):
    def __init__(self, observation_space: Any, action_space: Any, model_id='0', config=None, *args, **kwargs):
        self.model = None
        super(TFKerasModel, self).__init__(observation_space, action_space, model_id, config, *args, **kwargs)

    def set_weights(self, weights, *args, **kwargs) -> None:
        self.model.set_weights(weights)

    def get_weights(self, *args, **kwargs) -> Any:
        return self.model.get_weights()

    def save(self, path: Path, *args, **kwargs) -> None:
        self.model.save(path)

    def load(self, path: Path, *args, **kwargs) -> None:
        self.model.load(path)

    def forward(self, states: Any, *args, **kwargs) -> Any:
        return self.model.predict(states)

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        pass
