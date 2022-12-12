function [dist,path] = floyd_algo(mat,range)
% mat 代价矩阵
% range 数目等于停靠点数目加连接点数目，不包括目标数目
max_value = 100000000; % 可以作为无穷大值
% 初始化dist矩阵和path矩阵
[lin,col] = size(mat);
dist = zeros(lin,col);
path = zeros(lin,col);
for i = 1:lin
    for j = 1:col
        w = mat(i,j);
        if isnan(w) % 如果点点权值为无穷大
            dist(i,j) = max_value;
            path(i,j) = -1;
        else  % 如果点点权值非无穷大
            if w == 0  % 如果点点权值为0
                dist(i,j) = w;
                path(i,j) = -1;
            else  % 如果点点权值非0
                dist(i,j) = w;
                path(i,j) = i;
            end
        end
    end
end

% floyd 主体
for k = 1:col
    for i = 1:col
        if i ~= k
            for j = 1:col
                if j ~= k && i ~= j && dist(i,k)+dist(k,j)<dist(i,j)
                    dist(i,j) = dist(i,k)+dist(k,j);
                    path(i,j) = k;
                end
            end
        end
    end
end

% 解析dist和path 输出结果
% fprintf('最短路径规划如下：\n');
col = range; 
lin = range;
for i = 1:lin
    for j = 1:col
        if i ~= j
            each_path = [];
            k = j;
            while k~=-1
                each_path = [each_path k];
                k = path(i,k);
            end
            fprintf('第%d号顶点到第j号顶点的最短路径为：');
            num = size(each_path,2);
            for index = 1:num
                fprintf(' %d ',each_path(num+1-index));
            end
            fprintf('dist = %d\n',dist(i,j));
        end
    end
end
end
