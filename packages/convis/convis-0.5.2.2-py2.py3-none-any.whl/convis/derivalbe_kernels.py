import torch
from .variables import Parameter, default_resolution

class ExponentialKernel(torch.nn.Module):
    def __init__(self, tau = 0.01, n=0, amplification=1.0):
        self.tau = Parameter(tau)
        self.n = Parameter(n)
        self.amplification = Parameter(amplification)
    def forward(self):
        tau_in_steps = default_resolution.seconds_to_steps(tau)
        if n == 0:
            a = amplification/tau_in_steps
            length = min(max(int(-tau_in_steps*torch.log(resolution.filter_epsilon/a))+1.0,min_steps),max_length)
            if length <= 1:
                return torch.ones(1)
            if even is False and length%2 == 0:
                length += 1
            if even is True and length%2 == 1:
                length += 1
            t = torch.linspace(1.0,length,length)
            kernel =  torch.exp(-torch.linspace(0.4,length-0.6,length)/float(tau_in_steps))
            if normalize:
                kernel *=  a
        else:
            a = amplification
            length = (int(-tau_in_steps*torch.log(resolution.filter_epsilon/a))-n)
            if length > max_length:
                length = max_length
            if length <= 1:
                return torch.ones(1)
            if even is False and length%2 == 0:
                length += 1
            if even is True and length%2 == 1:
                length += 1
            t = torch.linspace(1.0,n*length,n*length)
            kernel = amplification * (n*t)**n * torch.exp(-n*t/tau_in_steps) / (torch.math.factorial(n-1) * tau_in_steps**(n+1))
        if torch.any(torch.array(kernel.shape) == 0):
            return torch.ones(1)
        return kernel

def gauss_filter_2d(x_sig,y_sig,normalize=False,resolution=None,minimize=False, even=False, border_factor=1.0):
    """
        A 2d gaussian.

        x_sig and y_sig are the standard deviations in x and y direction.

        if :py:obj:`even` is not None, the kernel will be either made to have even or uneven side lengths, depending on the truth value of :py:obj:`even`.
    """
    if resolution is None:
        resolution = default_resolution
    if x_sig == 0 or y_sig == 0:
        return np.ones((1,1))
    x_sig = resolution.degree_to_pixel(x_sig)
    y_sig = resolution.degree_to_pixel(y_sig)
    a_x = 1.0/(x_sig * np.sqrt(2.0*np.pi))
    x_min = border_factor*np.ceil(np.sqrt(-2.0*(x_sig**2)*np.log(resolution.filter_epsilon/a_x)))
    a_y = 1.0/(y_sig * np.sqrt(2.0*np.pi))
    y_min = border_factor*np.ceil(np.sqrt(-2.0*(y_sig**2)*np.log(resolution.filter_epsilon/a_y)))
    if x_min < 1.0:
        x_gauss = np.ones(2) if even else np.ones(1)
    else:
        X = np.arange(1.0-x_min-(0.5 if even else 0.0),x_min+(0.5 if even else 0.0))
        x_gauss = (a_x *np.exp(-0.5*(X)**2/float(x_sig)**2)).clip(0,1)
    if y_min < 1.0:
        y_gauss = np.ones(2) if even else np.ones(1)
    else:
        Y = np.arange(1.0-y_min-(0.5 if even else 0.0),y_min+(0.5 if even else 0.0))
        y_gauss = (a_y *np.exp(-0.5*(Y)**2/float(y_sig)**2)).clip(0,1)
    kernel = np.prod(np.meshgrid(x_gauss,y_gauss),0)
    if np.any(np.array(kernel.shape) == 0):
        return np.ones((1,1))
    return kernel