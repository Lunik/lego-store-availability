
class Store:
  hostname = "www.lego.com"

  def __init__(self, lang="fr-fr", insecure=False):
    self.lang = lang
    self.insecure = insecure

  @property
  def base_url(self):
    protocol = "http" if self.insecure else "https"

    return f"{protocol}://{self.hostname}/{self.lang}"