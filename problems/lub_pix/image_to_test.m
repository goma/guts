% Read image
IM = imread('tread.gif');

% Convert to grayscale
%IM = 0.2989*IM(:,:,1) ...
%   + 0.5870*IM(:,:,2) ...
%   + 0.1140*IM(:,:,3);
IM = double(IM);

% Calculate dimensions
xlen = 2.5;
IMsize = size(IM);
xn = IMsize(2);
yn = IMsize(1);
yx = yn/xn;
ylen = xlen*yx;
NN = xn*yn;

% Create coordinate mesh
xv = linspace(-xlen/2,xlen/2,xn);
yv = linspace(ylen/2,-ylen/2,yn);
[X,Y] = meshgrid(xv,yv);

% Rescale data from 0 to 1
maxI = max(max(IM));
minI = min(min(IM));
IM = -255.0/(maxI-minI).*IM + maxI*255.0/(maxI-minI);

% Plot image
figure(1);
colormap(gray(256));
image([0 xlen],[0 ylen],IM);

% Export data
fid = fopen('tread.txt','w');
fprintf(fid,'%i\n',NN);
for i = 1:xn
    for j = 1:yn
        fprintf(fid,'%e %e %e %e \n',xv(i),yv(j),0.0,IM(j,i));
    end
end
fclose(fid);
