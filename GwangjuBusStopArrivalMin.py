import requests
import json

# 210409 기준 키 없어도 정상작동
KEY = ""


# 버스 노선 정보
#busLineUrl = "http://api.gwangju.go.kr/xml/lineInfo?serviceKey="

# 버스정류장 ARS_ID를 정류장_ID로 변환
def BusStopId(arsId):
    # 버스 정류장 정보
    busStopInfomationUrl = "http://api.gwangju.go.kr/json/stationInfo?serviceKey="
    req = requests.get(busStopInfomationUrl)
    req = req.json()

    for BusStop in req["STATION_LIST"]:
        if arsId == BusStop["ARS_ID"]:

            return BusStop
            
        # # 레코드 구분
        # BusStopStationNum = BusStop["STATION_NUM"]
        # # 정류소 ID
        # BusStopID = BusStop["BUSSTOP_ID"]
        # # 정류소 명(국문)
        # BusStopKORName = BusStop["BUSSTOP_NAME"]
        # # 정류소 명(영문)
        # BusStopENGName = BusStop["NAME_E"]
        # # 위도
        # BusStopLongitudue = BusStop["LONGITUDE"]

# 해당 정류장에 버스 도착까지 몇 분 남았는가 가져오기
def BusArrival(busStopId):
    # 버스 도착 정보
    busArrivalInformationUrl = "http://api.gwangju.go.kr/json/arriveInfo?&BUSSTOP_ID="+str(busStopId)
    req = requests.get(busArrivalInformationUrl)
    req = req.json()
    BusSave = []
    for Arrival in req["BUSSTOP_LIST"]:
        temp = []
        RemainStop = Arrival["REMAIN_STOP"]     # 도착까지 남은 정류장 개수
        BusName = Arrival["SHORT_LINE_NAME"]    # 버스 이름
        #BusId = Arrival["BUSID"]                # 버스 ID
        #BusWhere = Arrival["BUSSTOP_NAME"]       # 현재 버스가 위치한 정류장 이름
        #BusWhereId = Arrival["CURR_STOP_ID"]    # 현재 버스가 위치한 정류장 번호
        #LineId = Arrival["LINE_ID"]             # 노선 번호
        BusArrivalNum = Arrival["REMAIN_MIN"]   # 도착 예정 시간
        #BusStart = Arrival["DIR_START"]         # 버스 기점
        #BusEnd = Arrival["DIR_END"]             # 버스 종점
        BusFlag = Arrival["ARRIVE_FLAG"]       # 0 : 일반 , 1 : 곧도착
        temp.append(BusName)        #버스명
        temp.append(BusArrivalNum)  #도착 예정시간
        temp.append(RemainStop)     # 도착까지 남은 정류장
        temp.append(BusFlag)        # 곧도착
        BusSave.append(temp)
    return BusSave

# 버스 남은시간 출력
def BusArrivalPrint(BusSave,BusStopName):
    print("<<",BusStopName,">>","정류장 정보")
    for i in range(len(BusSave)):
        if BusSave[i][3] == 1:
            print("[",BusSave[i][0],"] 도착까지 ",BusSave[i][1],"분 남았습니다.\t남은 정류장 개수:",BusSave[i][2],"(곧도착)")
        else:
            print("[",BusSave[i][0],"] 도착까지 ",BusSave[i][1],"분 남았습니다.\t남은 정류장 개수:",BusSave[i][2])

# 버스 정류장 번호 입력받기
print("정류장 번호를 입력하세요 :",end='')
busStopId = input()
# 버스 정류장 번호 (ARS번호를 ID로 변경)
busSave = BusStopId(busStopId)
busStopId = busSave["BUSSTOP_ID"]
# 해당 정류장에 버스 도착까지 몇분 남아있는가 출력
BusArrivalPrint(BusArrival(busStopId),busSave["BUSSTOP_NAME"])

