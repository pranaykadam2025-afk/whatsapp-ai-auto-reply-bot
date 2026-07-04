from google import genai

client = genai.Client(api_key="your_actual_api_key_here")
command= '''
[11:40 am, 26/06/2026] Pratik Pashte: Kr mg
[11:40 am, 26/06/2026] Pratik Pashte: Tuza mind ky bolt ahe
[11:42 am, 26/06/2026] Pranay Kadam: Karto
[12:35 pm, 26/06/2026] Pranay Kadam: Aryan ahe ka sobat ?
[8:26 pm, 26/06/2026] Pratik Pashte: 9 la ye mg
[8:26 pm, 26/06/2026] Pratik Pashte: Mi khali chalo ahe
[8:38 pm, 26/06/2026] Pranay Kadam: Tikdun nighala ki call kar mg yeto khali
[8:39 pm, 26/06/2026] Pratik Pashte: Tikdun nighala ki call kar mg yeto khali
Ha thike ahe
[9:41 pm, 26/06/2026] Pratik Pashte: Aalo ahe ghari

'''
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are a person named pranay  who speaks hindi as well as english . he is from  India and  is a coder . you analyze chat history and respond  like  pranay "
    },
    contents= command
)

print(response.text)