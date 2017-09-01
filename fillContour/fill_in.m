
savedir = './bin';
roidir = './roi';


subdir = dir(roidir);

for i = 1 : length( subdir )
    if( isequal( subdir( i ).name, '.' )||...
        isequal( subdir( i ).name, '..')||...
        subdir( i ).isdir)               
        continue;
    end

    img = imread([subdir(i).folder,'/',subdir(i).name]);
    img= img(:,:,3);
    level = graythresh(img);
    img= 1-im2bw(img,level);
    L = bwlabel(img);
    num_conn = max(max(L));
    mask = zeros(size(img));
    for j = 1:num_conn
        conn = (L==j)*1;
        if sum(sum(conn))<100 || conn(3,3) ~= 0
            continue
        end
        mask = mask + conn*100;
    end
    SE = strel('sphere',3);
    dilate = imdilate(mask,SE);
    imshow(dilate)
    
    imwrite(dilate,[savedir,subdir(i).name])

end




