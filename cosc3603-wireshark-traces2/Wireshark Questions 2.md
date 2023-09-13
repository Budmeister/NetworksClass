# Wireshark Questions 2
See the annotated documents. The color of the text matches with the color on the annotated documents where the answer was found.
1. <span style="color: #008204">My browser is running HTTP 1.1. The server is also running HTTP 1.1.</span> 
2. <span style="color: #eb4034">My browser indicates that it can accept html, xhtml+xml, and xml. It can accept image formats avif, webp, and apng.</span> 
3. <span style="color: #2a1b9e">My IP is 10.19.26.113. The server's IP is 128.119.245.12.</span> 
4. <span style="color: #1ff8ff">The server sent status code 200.</span>
5. <span style="color: #000000">The document was last modified at 6:02 on September 5.</span>
6. <span style="color: #c430ff">128 bytes were returned to my browser.</span>
7. <span style="color: #575757">The option, `Upgrade-Insecure-Requests` is not listed in the packet-listing window.</span>
8. No.
9. <span style="color: #008204">Yes, Wireshark lists the number of bytes of the file received.</span> 
10. <span style="color: #2a1b9e">Yes. It lists the time when it was retrieved the first time.</span> 
11. <span style="color: #eb4034">The server sent status code 304 without sending the whole file again, because Chrome indicated that it had a copy of the file and only needed a new copy if it had been updated on the server since the time when Chrome had received it.</span>
12. <span style="color: #2a1b9e">My browser only sent one GET request.</span>
13. <span style="color: #c430ff">The HTTP header data was included in the first TCP frame, Frame 349.</span>
14. <span style="color: #ff960d">The response status code was 200 OK.</span>
15. <span style="color: #008204">It took 4 TCP segments.</span>
16. <span style="color: #2a1b9e">My browser only sent 3 GET requests.</span>
17. <span style="color: #eb4034">It looks like the browser downloaded the two images serially, because it did not send the GET request for the second image until the first image was already received.</span>
18. <span style="color: #eb4034">The first response was 401 Unauthorized.</span>
19. <span style="color: #c430ff">It now has the field, `Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=`.</span>