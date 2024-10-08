from pygame.time import get_ticks

class Timer:
	def __init__(self,
            duration: float,
			func = None,
			repeat: bool = False
		) -> None:
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False
		self.repeat = repeat

	def activate(self) -> None:
		self.active = True
		self.start_time = get_ticks()
		return None

	def deactivate(self):
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()
		return None

	def update(self):
		if not self.active:
			return None
		current_time = get_ticks()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()
		return None
