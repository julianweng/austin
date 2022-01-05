# Readme for Chatbot

This is basd on https://github.com/JiteshGaikwad/Chatbot-Widget

## References

How I added the voices to the Chatbot Widget:

- https://github.com/mdn/web-speech-api/tree/master/speak-easy-synthesis
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/SpeechSynthesisUtterance
- https://mdn.github.io/web-speech-api/speak-easy-synthesis/
- https://www.studytonight.com/post/javascript-speech-recognition-example-speech-to-text

## Hot to get all the voices:
```
if (theVoice == null) {
    let voices = synth.getVoices();
    for(i = 0; i < voices.length ; i++) {
        if(voices[i].name === "Google UK English Male") {
            utterThis.voice = voices[i];
            theVoice = voices[i];
            console.log("Voice is set.");
            break;
        }
    }
}
```

## Get free background
https://unsplash.com/