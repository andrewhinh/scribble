# scribble

Comic Book Strip OCR and Text Generation

![image](https://user-images.githubusercontent.com/40700820/194950556-a095b6ac-3c11-478d-ac5e-9bf849d556dc.png)

Author's explanation [here](https://www.youtube.com/watch?v=-Z06KjGyqKI).

## Setup to Run a Gradio App Locally
1. Clone repo.
2. Create a python3 venv using `python3 -m venv env` and then `source env/bin/activate` or `<venv>\Scripts\activate.bat`, depending on your OS.
3. Run `make install` to download the dependencies.
4. Run `export COHERE_APIKEY=REPLACE`, replacing `REPLACE` with your Cohere API key.
5. Run `app.py` (with `--flagging` if you want to allow users to flag generations as incorrect, offensive, etc.), and you now have a local Gradio app!

## Notes
- Project for the TAMU Datathon to solve the [CBRE Challenge: Get in Line](https://tamudatathon.com/challenges/docs/cbre) and the [Best Use of NLP by Cohere - MLH](https://tamudatathon.com/challenges/docs/mlh_challenges#best-use-of-nlp-by-cohere---mlh) challenges.
- When evaluated with difflib.SequenceMatcher on the challenge-provided files found [here](https://tamudatathon.com/challenges/assets/files/training-strips-3b6c286bdfd746b25ebd59e2225c0b50.zip), the OCR model achieves ~89% average accuracy for all the example comic strips.
- Since we are open-sourcing the necessary code for others to create their own Gradio link, please be mindful of what data you submit to others' links and the privacy of the data people submit to your links.

## Credit
- Tesseract for their [OCR engine](https://github.com/tesseract-ocr/tesseract).
- [Cohere.ai](https://cohere.ai/) for their text generation API.
