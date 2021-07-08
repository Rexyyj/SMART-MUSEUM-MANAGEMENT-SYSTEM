readChannelID = [];
hList = [];
zoneList =[];
avgList = [];
listUri = "https://api.thingspeak.com/users/kaih0802/channels.json";
requests = matlab.net.http.RequestMessage;
requests.Method = 'get';
[response, completedReq, history] =send(requests,listUri);
channelNum = length(response.Body.Data.channels);
for i = 1:channelNum
    readChannelID = [readChannelID,response.Body.Data.channels(i,1).id];
end
    pause(1)
for i = 1:length(readChannelID)
    [T,info]= thingSpeakRead(readChannelID(i),'Fields',[1,3],'NumMinutes',60,'OutputFormat','TimeTable');
    m = mean(T{:,1});
    t= datetime();
    h = hour(t)-1;
    zone = string(info.Name);
    hList =[hList,h];
    zoneList =[zoneList,zone];
    avgList = [avgList,m];
    pause(1)
    disp("Finish a static...")
end
tStamps = [datetime('now'):minutes(1):datetime('now')+minutes(length(readChannelID)-1)]';
dataTable = timetable(tStamps,hList',zoneList',avgList');
thingSpeakWrite(1421349,dataTable, 'WriteKey', 'SKRQKKMJCUQLTZBI');