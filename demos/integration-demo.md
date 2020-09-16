# Tidepool integration for Semantic Containers
A single Linux host integration demo for MyPCH.

You will need to install three components to get the demo working. The 
documentation for each of these components are found here (we will 
use upstream versions of the projects for this demo):

[Tidepool uploader](https://github.com/tidepool-org/uploader)

[Tidepool development](https://github.com/tidepool-org/development)

[Semantic container](https://github.com/sem-con/sc-diabetes)

# Install Tidepool client
Install uploader client (electron app), an extraction utilty of medical device suppported by Tidepool.

Detailed instructions are available in [prepare](prepare/getstarted.md) or at [tidepool uploader](https://github.com/tidepool-org/uploader).

Short instructions is to establish the build dependencies 
(gcc g++ make libavutil-dev libsecret-1-dev libudev-dev git curl 
liblzo2-dev) and to install nvm. Then after cloning the project 
one will have to do:

```
REL=24d52b1dc19e5fc11d60e3af5ad0cbd5d43d2265
git clone https://github.com/tidepool-org/uploader.git
cd uploader
git co $REL
nvm install 12
nvm use 12
npm install
npm install yarn -g
source config/local.sh
yarn install
yarn dev
```

This will bring up the client in a mode where it will complain 
about the missing open ports that the backend will provide once
its up and running.

# Install Tidepool backend 
Install backend (emulated kubernetes cluster and 27 backend pods for the platform): 

Detailed instructions are available in [prepare](prepare/getstarted.md) or at 
[tidepool development](https://github.com/tidepool-org/development).

Short instructions after establishing pre-requisite and cloning the 
project:

```
tidepool-server start
tidepool-server-set-config
tidepool start
```

```
kubectl get pods
NAME                              READY   STATUS      RESTARTS   AGE
auth-6fdf57b44b-l5hxb             1/1     Running     0          2m11s
blip-56558cb7db-8tnph             1/1     Running     0          2m11s
blob-6dd656f7b4-5x29p             1/1     Running     0          2m11s
data-56699998b6-r6rb5             1/1     Running     0          2m10s
discovery-fc4f964cd-hfbgl         1/1     Running     0          2m18s
export-669d4fd454-2gctv           1/1     Running     0          2m10s
gatekeeper-67894b6999-dt8kn       1/1     Running     0          2m10s
gateway-5d9cd74bf9-fcpgp          1/1     Running     0          2m18s
gateway-certgen-kglgh             0/1     Completed   0          2m17s
gateway-proxy-69488cbc9b-ng8ps    1/1     Running     0          2m18s
gloo-5cdcc7cd68-rzpc5             1/1     Running     0          2m19s
highwater-894485cdf-t45vf         1/1     Running     0          2m9s
hydrophone-5c578f8fdd-6llhv       1/1     Running     0          2m9s
image-887484cb9-k7cx7             0/1     Running     0          2m9s
jellyfish-7d748875bb-vmclm        1/1     Running     0          2m9s
message-api-858b7cc4db-ppkpp      1/1     Running     0          2m8s
migrations-f4f5d4987-ztpth        1/1     Running     0          2m8s
mongodb-556897c9f4-p6sjw          1/1     Running     0          2m20s
nosqlclient-6b56bff8f6-sjmcb      1/1     Running     0          2m7s
notification-686dd79f84-f5k8x     1/1     Running     0          2m7s
seagull-6869d769cb-8l7tf          1/1     Running     0          2m6s
shoreline-5fb55d6859-jqqcg        1/1     Running     0          2m6s
task-5578847fd5-ngrnd             1/1     Running     0          2m5s
tide-whisperer-6869c6b89c-tdmjm   1/1     Running     0          2m5s
tools-86cdfb4856-678ks            1/1     Running     0          2m4s
user-68467dbdd9-49dbz             1/1     Running     0          2m4s
```

Ensure that external k8s services are available to the client:

```
jellyfish=$(kubectl get pods|grep jellyfish|awk '{print $1}')
kubectl port-forward $jellyfish 9122:9122
```

```
data=$(kubectl get pods|grep 'data\-'|awk '{print $1}')
kubectl port-forward $data 9220:9220
```

```
blip=$(kubectl get pods|grep 'blip'|awk '{print $1}')
kubectl port-forward $blip 3000:3000
```

Finally confirm that kubernetes ports are open to the client outside 
of to the cluster:

```
netstat -atn|grep LISTEN|grep 9122
tcp        0      0 127.0.0.1:9122          0.0.0.0:*               LISTEN     
tcp6       0      0 ::1:9122                :::*                    LISTEN     
netstat -atn|grep LISTEN|grep 3000
tcp6       0      0 :::3000                 :::*                    LISTEN     
netstat -atn|grep LISTEN|grep 9220
tcp        0      0 127.0.0.1:9220          0.0.0.0:*               LISTEN     
tcp6       0      0 ::1:9220                :::*                    LISTEN     
```

# Integrate Tidepool client and backend
Confirm integration between electron client and backend platform.

Lets sign up a user and upload some device data for this user using 
the electron uploader app.

```
Adjust config/local.sh:
export API_URL='http://localhost:3000'
export UPLOAD_URL='http://localhost:9122'
export DATA_URL='http://localhost:9220'
export BLIP_URL='http://localhost:3000'
```

```
xdg-settings set default-web-browser chromium-browser.desktop
source config/local.sh
yarn dev
```

```
tidepool verify-account-email jl@ds.dk 
```

# Tidepool GET/POST interactions between client and backend
Redo GET/POST interactions between client and backend from the CLI 

Assuming that user jl@ds.dk has signed up. We can now interact with the 
platform as this user. First get credentials:

```
curl -v -X POST -u jl@ds.dk http://localhost:3000/auth/login >> login.log 2>&1
TPID=$(grep userid login.log |awk -F',' '{print $(NF-1)}'|awk -F':' '{print $2}')
TPTOKEN=$(grep x-tidepool-session-token login.log |awk -F',' '{print $(NF-1)}'|awk -F':' '{print $2}')
```

## POST data to the backend via curl:

```
cat record.json | \
     curl -X POST -d @- \
         -H "Content-Type: application/json" \
         -H "x-tidepool-session-token: $TPTOKEN" \
         http://localhost:3000/data/$TPID

```

## GET data from backend via curl:

```
curl -s -X GET -H "x-tidepool-session-token: $TPTOKEN" \
               -H "Content-Type: application/json" \
               "http://localhost:3000/data/$tpid" > out.json
```

# Add an SC component for data watermarking
Assuming the SC runs at port 4000. From the CLI on would do something along these lines:

```
 SC_IMAGE=semcon/sc-diabetes:latest; \
 docker run -d --name df1_pwd_local -p 4000:3000 \
     -e IMAGE_SHA256="$(docker image ls --no-trunc -q $SC_IMAGE | cut -c8-)" \
     -e IMAGE_NAME=$SC_IMAGE -e WATERMARK=true \
     $SC_IMAGE /bin/init.sh "$(< df1_pwd_local_init.trig)"

 APP_KEY=`docker logs df1_pwd_local 2>/dev/null | grep ^APP_KEY | awk -F " " '{print $NF}'`; \
 APP_SECRET=`docker logs df1_pwd_local 2>/dev/null | grep ^APP_SECRET | awk -F " " '{print $NF}'`; \
 export PWD_TOKEN_LOCAL=`curl -X POST -s -d grant_type=client_credentials \
     -d client_id=$APP_KEY -d client_secret=$APP_SECRET -d scope=admin \
     http://localhost:4000/oauth/token | jq -r '.access_token'`

 cat record.json | \
     curl -X POST -d @- \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer $PWD_TOKEN_LOCAL" \
         http://localhost:4000/api/data
```

And the SC_IMAGE would automatically repost the watermarked record (so it would have 
to know the relevant TPTOKEN and FORWARDURL and then do something like this:

```
cat WATERMARKED(record.json) | \
     curl -X POST -d @- \
         -H "Content-Type: application/json" \
         -H "x-tidepool-session-token: $TPTOKEN" \
         $FORWARDURL 
```

# Prerequistite of SC
To work, the SC component shall support:

1) Add two state variables to the SC: TPTOKEN, FORWARDURL. These state variable shall be set when launching the image.

2) Automatically forward post call to FORWARDURL as described in the curl call above with watermarked data.

# Final verification 

Let us now mimic the last data flow. Let Ti denote terminal i:

```
T1: tcpdump -i lo -vv -n host 192.168.1.11 and port 4010
T2: netcat -l 4010
```

Finally in T3 (assuming that the backend runs at 192.168.1.11), lets do:

```
git clone https://github.com/sem-con/sc-diabetes.git
cd sc-diabetes/test
SC_IMAGE=semcon/sc-diabetes:latest; \
  docker run -d --name forward -p 4000:3000 \
      -e IMAGE_SHA256="$(docker image ls --no-trunc -q $SC_IMAGE | cut -c8-)" \
      -e IMAGE_NAME=$SC_IMAGE -e WATERMARK=true \
      -e FORWARDURL=http://192.168.1.11:4010/api/data -e TPTOKEN=123 \
      $SC_IMAGE /bin/init.sh "$(< forward_init.trig)"
sleep 30 # as per doc from Christoph
APP_KEY=`docker logs forward 2>/dev/null | grep ^APP_KEY | awk -F " " '{print $NF}'`; \
APP_SECRET=`docker logs forward 2>/dev/null | grep ^APP_SECRET | awk -F " " '{print $NF}'`; \
export PWD_TOKEN_LOCAL=`curl -X POST -s -d grant_type=client_credentials \
-d client_id=$APP_KEY -d client_secret=$APP_SECRET -d scope=admin \
http://localhost:4000/oauth/token | jq -r '.access_token'`
echo $PWD_TOKEN_LOCAL
cat data.json | curl -X POST -d @- \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $PWD_TOKEN_LOCAL" \
      http://192.168.1.11:4000/api/data
```

Then in T2, we find:

```
netcat -l 4010                                                                                                                                                
POST /api/data HTTP/1.1                                                                                                                                                                                           
Content-Type: application/json                                                                                                                                                                                    
X-Tidepool-Session-Token: 123
Connection: close
Host: 192.168.1.11:4010
Content-Length: 1145
[{"deviceId":"InsOmn-130130814","type":"smbg","units":"mmol/L","time":"2015-12-02T12:13:44","id":"ahmmvi0dsl31lvg4eehjljnn80m7ii7e","value":7.068554201187744},{"deviceId":"DexG4Rec_SM45143452","type":"deviceEvent","units":"mmol/L","time":"2015-12-02T12:16:06","id":"5j6ribjsv0jtp063fi9dc26fqnn1er9a","value":7.389567648790684},{"deviceId":"InsOmn-130130814","type":"smbg","units":"mmol/L","time":"2015-12-02T13:22:59","id":"q05vehd9l9feodg6u3dd3co1cbqui31u","value":9.23171496099094},{"deviceId":"DexG4Rec_SM45143452","type":"deviceEvent","units":"mmol/L","time":"2015-12-02T13:25:17","id":"pr3bufbri2pm5ufidtncdra8m0qf4a86","value":9.467005412494094},{"deviceId":"InsOmn-130130814","type":"smbg","units":"mmol/L","time":"2015-12-02T13:51:37","id":"b0rq8919f90is0embtp00vb1mmv3r7aq","value":9.11289254522036},{"deviceId":"DexG4Rec_SM45143452","type":"deviceEvent","units":"mmol/L","time":"2015-12-02T13:54:11","id":"crg24hg0krjjl4hnc8a4akmgr5pq4b77","value":9.651373921880788},{"deviceId":"DexG4Rec_SM45143452","type":"deviceEvent","units":"mmol/L","time":"2015-12-02T13:54:27","id":"r4rguco0ghdsoiimuhnsi1jm7b2fcttb","value":9.063380508918236}](base) x@x:~/check-out/ds/sc-diabetes/test$ head data.json 
[
  {
    "deviceId": "InsOmn-130130814",
    "type": "smbg",
    "units": "mmol/L",
    "time": "2015-12-02T12:13:44",
    "id": "ahmmvi0dsl31lvg4eehjljnn80m7ii7e",
    "value": 7.265967376079979
  },
  {
```

If we cross-compare the input that we provide with the data delivered by the
backend we can confirm that the numbers in the backend are indeed watermarked:

```
cat from_container.json | jq .|grep val
    "value": 7.068554201187744
    "value": 7.389567648790684
    "value": 9.23171496099094
    "value": 9.467005412494094
    "value": 9.11289254522036
    "value": 9.651373921880788
    "value": 9.063380508918236
cat data.json | jq .|grep val
    "value": 7.265967376079979
    "value": 7.203457871058321
    "value": 9.367337579771725
    "value": 9.364481206095553
    "value": 9.2685817575144
    "value": 9.4844807308652
    "value": 9.185249148474703

paste v1.txt v2.txt |sed 's;\t; ;g'|awk '{print $1 " " $2 " " $1-$2}'
7.265967376079979 7.068554201187744 0.197413
7.203457871058321 7.389567648790684 -0.18611
9.367337579771725 9.23171496099094 0.135623
9.364481206095553 9.467005412494094 -0.102524
9.2685817575144 9.11289254522036 0.155689
9.4844807308652 9.651373921880788 -0.166893
9.185249148474703 9.063380508918236 0.121869
```
