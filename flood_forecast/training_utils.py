import torch


class EarlyStopper(object):
    """EarlyStopping handler can be used to stop the training if no improvement after a given number of events.
    Args:
        patience (int):
            Number of events to wait if no improvement and then stop the training.
        score_function (callable):
            It should be a function taking a single argument, an :class:`~ignite.engine.Engine` object,
            and return a score `float`. An improvement is considered if the score is higher.
        trainer (Engine):
            trainer engine to stop the run if no improvement.
        min_delta (float, optional):
            A minimum increase in the score to qualify as an improvement,
            i.e. an increase of less than or equal to `min_delta`, will count as no improvement.
        cumulative_delta (bool, optional):
            It True, `min_delta` defines an increase since the last `patience` reset, otherwise,
            it defines an increase after the last event. Default value is False.
    Examples:
    .. code-block:: python
        from ignite.engine import Engine, Events
        from ignite.handlers import EarlyStopping
        def score_function(engine):
            val_loss = engine.state.metrics['nll']
            return -val_loss
        handler = EarlyStopping(patience=10, score_function=score_function, trainer=trainer)
        # Note: the handler is attached to an *Evaluator* (runs one epoch on validation dataset).
        evaluator.add_event_handler(Events.COMPLETED, handler)
    """

    def __init__(
        self,
        patience: int,
        min_delta: float = 0.0,
        cumulative_delta: bool = False,
    ):

        if patience < 1:
            raise ValueError("Argument patience should be positive integer.")

        if min_delta < 0.0:
            raise ValueError("Argument min_delta should not be a negative number.")

        self.patience = patience
        self.min_delta = min_delta
        self.cumulative_delta = cumulative_delta
        self.counter = 0
        self.best_score = None

    def check_loss(self, model, validation_loss) -> bool:
        score = validation_loss
        if self.best_score is None:
            self.save_model_checkpoint(model)
            self.best_score = score

        elif score + self.min_delta >= self.best_score:
            if not self.cumulative_delta and score > self.best_score:
                self.best_score = score
            self.counter += 1
            print(self.counter)
            if self.counter >= self.patience:
                return False
        else:
            self.save_model_checkpoint(model)
            self.best_score = score
            self.counter = 0
        return True

    def save_model_checkpoint(self, model):
        torch.save(model.state_dict(), "checkpoint.pth")

#test