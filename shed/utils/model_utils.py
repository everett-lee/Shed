def load_model(model_path, device=None):
    import torch

    agent = torch.load(model_path, map_location=device)
    agent.set_device(device)

    return agent

