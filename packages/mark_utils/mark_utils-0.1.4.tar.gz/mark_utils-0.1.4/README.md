# Utils
For every python programmer arrive the moment to create his packages.
This is my utils repo.

## Includes:

## Preprocessing:
Some preprocessing util functions:

* Features matrix
    - Standardize (numpy, pytorch)
    - Normalize   (numpy, pytorch)

## PCA
Calculate the PCA (numpy, pytorch)

## Scraper
Wrapper for manager a FireFox browser with selenium library.

## Pcap Analyzer
Wrapper for analyze the .pcap file. This first version return a list of dictionary, further version will also returns numpy.narray and pandas dataframe format. Limited only for IPv4. If someone want improve it to ipv6
will be appreciated.

Analyze:  
          -   [frame] -> Datalink Layer   / OSI 2
          -   [packet] -> Network Layer   / OSI 3
          -   [segment/datagram] -> Transport Layer / OSI 4


email:  marcotreglia1@gmail.com


# Usage
* Preprocessing

```python
from mark_utils.preprocessing import Standardize, Normalize

# Numpy
x = np.random.rand(100,5)
x = Standardize.numpy(x)
x = Normalize.numpy(x)

# Pytorch (cuda enable)
x = torch.randn(100,5)
x = Standardize.torch(x)
x = Normalize.torch(x)
```

* PCA

```python
from mark_utils.pca import PCA

# Numpy
x = np.random.rand(100,5)
x_pca = PCA.numpy(x)

# Pytorch (cuda enable)
x = torch.randn(100,5)
x_pca = PCA.torch(x)
```

* Scraper

```python
from mark_utils.scraper import Scraper

# Init the browser
s = Scraper()

# Open url (For fun let's scrab some rocks!)
s.openUrl('http://www.radiofreccia.it/fm/')

# set target (In this case is the artist of the current song)
# create a dictionary with :  
# type: [xpath, class, id, tag, link] |  name : 'respectively target'

artist = dict(type='xpath', name='(//*[@class="white first-line"])[1]')

# Get the element from the webBrowser
element = s.get_element_BY(title)
print(artist_element.text)
'Imagine Dragons'

# Or if you want multiple element you can do :
title = dict(type='xpath',name='(//*[@class="white second-line"])[1]')
target_list = [artist, title ]
elements = s.get_element_BY(target_list)
for e in elements:
  print(e.text)

'Imagine Dragons'
'Thunder'

```

* Pcap Analyzer

```python
from mark_utils.pcap import PcapAnalyzer

pcap_file = 'path/Dump.pcap'
infos = PcapAnalyzer.to_dict(pcap_file)

print(infos[0])

"{'DATALINK': {'destination': '00:00:00:5A:F2:C8',
  'proto': 8,
  'source': '00:00:00:00:00:E4'},
 'NETWORK': {'header_len': 20,
  'proto': 6,
  'protocol': 'IPV4',
  'source': '173.194.165.233',
  'target': '192.168.0.7',
  'ttl': 57,
  'version': 4},
 'TRANSPORT': {'ack': 0,
  'destination': 56981,
  'flags': {'ack': 0, 'fin': 0, 'psh': 0, 'rst': 0, 'syn': 0, 'urg': 0},
  'protocol': 'TCP',
  'sequence': 4110851931,
  'source': 443},
 'data': b'Uv\xdf{\xdeL\xfc \x90\x12\xfe\xcdh\x87\xfc\x94Y\x03\x17\x8c\xbb\xecN\xf8\xad\xce\x11\xf9T\xe7$\rK\xca\xd9\x11\xf76\xd8\xd0"Nb\xa0T\xea\x03\xaf(5\xb5TP\x96W;\x96\xa5\x9c#\xe9\xf4\xdc\xc6\xd9A)?\xa2\xb5\x1e\xc3k\xd5B,T\n\xf4t\xcd\xa0\xe6We+\x0c\x994\x11\x17\x8d\xbbK\xae\xe0c\xe0\xc7\xb8\xf1!\xe3S$q\xae\xb6\x88\x9fn\xc32r\x05\x04\xd5\xc4\xfd\xf7\xed\xb1\xde\x93\xd0\x995j\xaf1|\x0bw%~\xebc\xc1\x8cg\x17\x0f\x1c\xed\xd5C\xcf:@\x07K\xffC\xd3\xe3i\xdakja\x1d>nxV\x83$\xb3\xaf\x17\x94\x03VZy\x15S\n@\x19.\x1c\x13\xee\x10\xaf_[\x8dn\x12\x97\x ... ... ... "


```

versione: 0.1.2
