let socket = io('http://140.117.71.98:4001')
const constraints = {'video': true, } 
const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]}
const peerConnection = new RTCPeerConnection(configuration);
let localStream; 
let videoElement;

peerInit();
setUpListener();

async function peerInit(){
	peerConnection.createDataChannel('stream');
	localStream = await navigator.mediaDevices.getUserMedia(constraints);
	videoElement = document.querySelector('video#localVideo');
	videoElement.srcObject = localStream;
	localStream.getTracks().forEach(track => {
		console.log(track);
		peerConnection.addTrack(track, localStream);
		console.log('add trak to peerconnection')
	});
}

async function setUpListener(){
	socket.on('rtc-message', getAnswerAndSetRemote);
	peerConnection.addEventListener('icecandidate', getIceCandidateAndSend);
	socket.on('rtc-message', getRemoteIceCandidateAndAdd);
	peerConnection.addEventListener('connectionstatechange', successConnected);
	socket.on('rtc-message', sendStreaming);
}

// get signal and start connection
async function sendStreaming (message) {
	message = JSON.parse(message);
	if (message.start) {  
		sendOffer();
	}
}

async function sendOffer(){
	const offer = await peerConnection.createOffer();
	console.log('create offer')
	await peerConnection.setLocalDescription(offer);
	socket.emit('rtc-message', JSON.stringify({'offer' : offer}));
	console.log('send offer')
}

async function getAnswerAndSetRemote (message){
	message = JSON.parse(message);
	if (message.answer) {  
		const remoteDesc = new RTCSessionDescription(message.answer);
		await peerConnection.setRemoteDescription(remoteDesc);
		console.log('setRemoteDescription finished');
	}
}

async function getIceCandidateAndSend (event) {
	if (event.candidate) {
		console.log('get IceCandidate')
		socket.emit('rtc-message', JSON.stringify({'new-ice-candidate': event.candidate}));
	}
}

async function getRemoteIceCandidateAndAdd (message) {
	message = JSON.parse(message);
	if (message["new-ice-candidate"]) {
		try {
			console.log('recieve IceCandidate from remote')
			await peerConnection.addIceCandidate(message["new-ice-candidate"]);
		} catch (e) {
			console.error('Error adding received ice candidate', e);
		}
	}
}

async function successConnected () {
	console.log(`current state ${peerConnection.connectionState}`)
	if (peerConnection.connectionState === 'connected') {
		console.log('peer connected!');
	}
}