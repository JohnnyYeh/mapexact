clear;
clc

mask = importdata('.\szmap\mask.csv'); # data.csv 换名而已
nodePos =  importdata('.\szmap\RoadVertexPosData.csv');
stoppingPos = importdata('.\szmap\StoppingPointPosData.csv');
customerPos = importdata('.\szmap\CustomerPosData.csv');

depotPos = stoppingPos(1:3,:);
stoppingPos = stoppingPos(4:end,:);
scatter(depotPos(:,1),depotPos(:,2),100,'s','filled');hold on;
scatter(stoppingPos(:,1),stoppingPos(:,2),100,'s','filled');hold on;
scatter(customerPos(:,1),customerPos(:,2),50,'filled');
scatter(nodePos(:,1),nodePos(:,2),10,'filled');
set(gca,'Ydir','reverse')

stoppingRoadNode = [depotPos;stoppingPos;nodePos];
depotNum = 3;
customerNum = length(customerPos);
nodeNum = length(nodePos);
stoppingNum = length(stoppingPos)+depotNum;
num = length(stoppingRoadNode)

for i = 1: customerNum
    str=sprintf('%d',i);
    text(customerPos(i,1)+4,customerPos(i,2)+8,str);
end

for x = 1: num
    for y = 1:num
        if(mask(x,y) == 1)
             plot([stoppingRoadNode(x,1),stoppingRoadNode(y,1)],...
                [stoppingRoadNode(x,2),stoppingRoadNode(y,2)],'r') ;
        end
    end
    str=sprintf('%d',x);
    text(stoppingRoadNode(x,1)+4,stoppingRoadNode(x,2)+8,str);
end

dist = nan*ones(num,num);
for x = 1:num
    for y = 1:num
        if(mask(x,y) == 1)
                diff = stoppingRoadNode(x,:)-stoppingRoadNode(y,:);
                dist(y,x) =norm(diff);
                dist(x,y) = dist(y,x);
        end
    end
    
end

[dist2,path] = floyd_algo(dist,stoppingNum);
 