# 한국어 발음을 벡터로 나타내기
### Train
* 한국어 단어 리스트를 학습 데이터로 사용 
* KoG2P로 주어진 한국어 단어를 IPA로 전사 
  * ex) ```박물관``` → ```p0 aa ng mm uu ll k0 wa nf```
* 각 IPA 기호와 phonetic features를 매핑 
  * ex) ```p0``` → ```(bilabial, stop, plain, voiced)```
  * ex) ```aa``` → ```(center, unrounded, low, vowel)```
* IPA 기호들의 bigram을 구하고 bigram 내 phonetic features 모든 조합을 구함 
  * ex) ```(p0, aa)``` → ```[bilabial-center, bilabial-unrounded, bilabial-low, bilabial-vowel, stop-center, ..., voiced-vowel]```
* (phonetic features 조합의 가짓수, 학습 단어의 가짓수) 크기의 행렬 생성 
  * ```(i,j)``` 성분은 ```i```번째 조합(ex. ```bilabial-center```)이 ```j```번째 단어(ex. ```박물관```)에서 사용된 빈도
* PCA로 원하는 크기로 차원 축소하여 각 phonetic features 조합을 표현하는 벡터 구함 
### Inference
* KoG2P로 주어진 한국어 단어를 IPA로 전사 
  * ex) ```박물관``` → ```p0 aa ng mm uu ll k0 wa nf```
* 각 IPA 기호와 phonetic features를 매핑 
  * ex) ```p0``` → ```(bilabial, stop, plain, voiced)```
  * ex) ```aa``` → ```(center, unrounded, low, vowel)```
* IPA 기호들의 bigram을 구하고 bigram 내 phonetic features 모든 조합을 구함 
* ```(주어진 단어에서 가능한 phonetic features 조합을 표현하는 벡터들의 평균) * (주어진 단어의 음절 수)``` 를 최종 phonetic vector로 사용 

## Examples 
<img src="https://github.com/yeounyi/korean-phonetic-vectors/blob/main/data/example.png?raw=true">
<br>

## Korean IPA to phonetic features with descriptions
https://docs.google.com/spreadsheets/d/1Gzz2SS9sV59DgZlvH_HA2Qh4hFiTKThLOam5nuuhRdw/edit?usp=sharing

## References 
* https://github.com/aparrish/phonetic-similarity-vectors
* https://github.com/scarletcho/KoG2P

## Data
* https://github.com/acidsound/korean_wordlist
