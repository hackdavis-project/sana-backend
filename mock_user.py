# mock script to insert mock information into the database

from modules import database
import asyncio
from modules import gemini


entries = [
  {
    "entry_text": "He was screaming again last night because dinner wasn't ready exactly on time. He didn't touch me, but he punched the wall right next to my head. Said it was my fault for provoking him. I'm so tired of being scared in my own home. Pretended I was asleep when he came to bed."
  },
  {
    "entry_text": "It's the constant criticism that gets me down. Nothing I ever do is right. 'You're too sensitive,' 'You can't take a joke,' 'Why are you always messing things up?' It chips away at you until you start believing it. I feel so small."
  },
  {
    "entry_text": "Had a dream about being a kid again. Locked in that closet. It felt so real. Woke up sweating. Why does it still affect me so much after all these years? I just want to forget but it feels like it's always there under the surface."
  },
  {
    "entry_text": "That guy at the party wouldn't leave me alone. Kept touching my arm, my back, even after I told him to stop. I felt trapped and just froze. Managed to get away eventually but I feel disgusting and shaky. Why do people think that's okay?"
  },
  {
    "entry_text": "Ever since the accident, I jump at every loud noise. Keep having flashbacks of the impact. Driving feels terrifying now. I just feel anxious all the time, like something bad is about to happen again."
  },
  {
    "entry_text": "It's Dad's birthday next week. First one without him. The thought just makes my chest ache. I miss his stupid jokes and how he always knew how to make me feel better. It just feels unfair."
  },
  {
    "entry_text": "Found another nasty anonymous comment on my profile today. It's the third one this week. They know exactly what buttons to push. Makes me want to just delete everything and hide. Why are people so cruel online?"
  },
  {
    "entry_text": "He controls all the money. I have to ask for everything, even just for bus fare. He looks through my receipts. Makes me feel like a child. I have a job but my paycheck goes straight into the account he manages. I have no freedom."
  },
  {
    "entry_text": "Just feeling really down today. Overwhelmed. Don't have the energy to do anything. Wish I could just sleep."
  },
  {
    "entry_text": "My daughter keeps asking for money, says she's in trouble again. I want to help but my social security barely covers my own rent and medicine. She gets so angry and makes me feel guilty if I hesitate. I'm worried she'll stop visiting if I say no."
  },
  {
    "entry_text": "Tried to talk about how hurt I was when they said that thing yesterday. They just laughed and told me I was remembering it wrong and being dramatic. Now I'm second-guessing myself. Did it even happen the way I thought? It's messing with my head."
  },
  {
    "entry_text": "My supervisor cornered me by the copier again today. Stood way too close, made some 'joke' that wasn't funny. I just mumbled something and left but my heart was pounding. I hate going to work now."
  },
  {
    "entry_text": "Tired."
  },
  {
    "entry_text": "Need to remember to pick up groceries after work tomorrow. Milk, bread, eggs."
  },
  {
    "entry_text": "It all feels so heavy. Like I can't breathe sometimes. What's the point of trying when everything just keeps going wrong? I really don't know how much more I can take. It feels like there's no way out."
  },
  {
    "entry_text": "It’s the cycle that messes with my head the most. Things will be tense, the walking on eggshells gets unbearable, then there's an explosion – maybe yelling, maybe something thrown (never me, not yet anyway), maybe just that terrifying silent treatment where he acts like I don't exist. Then, afterwards, he's suddenly so sorry, so loving, brings flowers, promises it won't happen again, tells me how much he needs me. And that's the part that keeps me here, I think. That glimpse of the person I fell in love with. But the tension always comes back, and I know the explosion is coming again. It's exhausting trying to predict it, trying to prevent it. I feel like I'm losing myself trying to manage his moods."
  },
  {
    "entry_text": "She has this way of twisting everything. We'll be having a normal conversation, and suddenly I'm defending myself against accusations that make no sense. She brings up things from years ago, takes things I said completely out of context, tells me I'm crazy or manipulative for feeling hurt by something she did. It happens so often that sometimes I genuinely start to doubt my own memory and perception. Am I the problem? It feels like trying to argue with fog – you can't grab onto anything solid, and you just end up lost and confused. It makes me hesitant to bring up any issues because I know it will somehow end up being my fault."
  },
  {
    "entry_text": "I was looking through old photos, trying to find one for grandma's birthday, and found pictures from when I was about 8 or 9. I look so serious in all of them. It brought back memories of how chaotic things were back then – the constant moving, never knowing where we'd be staying, sometimes skipping meals because the money ran out before payday. Mom did her best, I guess, but she was dealing with her own stuff. It wasn't physical abuse, more just... instability and neglect. Feeling responsible for things no kid should worry about. Seeing those pictures made me realize how much that time probably shaped the anxiety I feel now, always waiting for the other shoe to drop."
  },
  {
    "entry_text": "I finally told my best friend what happened. It was so hard, the words felt stuck in my throat. She was amazing, totally supportive, didn't push for details I wasn't ready to share. But now... now I feel this weird guilt, like I've burdened her with it. And part of me is terrified she sees me differently now, like I'm damaged goods. I know that's not fair to her, she's been great, but the fear is there. It makes me want to pull away, even though she's the one person I've trusted with this. Why is healing so complicated?"
  },
  {
    "entry_text": "I know it's irrational, but ever since that wildfire evacuation last year, I have this constant, low-level hum of anxiety. Every time the wind picks up or I smell smoke from someone's BBQ, my heart starts racing. I find myself checking the CAL FIRE website obsessively, even when there's no real threat nearby. I've double-checked my emergency bag countless times. Rationally, I know we're safe right now, here in Davis, but part of my brain is always on high alert, scanning for danger. It's interfering with my sleep and making it hard to just relax and enjoy a normal day."
  },
  {
    "entry_text": "My 'mentor' on this project seems determined to undermine me. In team meetings, she interrupts me constantly, corrects tiny, insignificant details in my work in front of everyone, and takes credit for ideas I shared with her privately. When I try to talk to her about it, she acts like I'm being overly sensitive or misunderstanding. It's subtle enough that reporting it feels risky – like I'll just look like I can't handle constructive criticism. But it feels personal and targeted. It's making me doubt my abilities and dread collaborating on anything."
  },
  {
    "entry_text": "Went to our favorite coffee shop today for the first time since he passed. Sat at 'our' table. It was harder than I expected. Everyone else was chatting and laughing, and it felt like I was in a bubble. Just kept expecting him to walk in. Left after five minutes."
  },
  {
    "entry_text": "Feeling completely burned out from school and work. Like my brain just won't function anymore. I keep procrastinating on big assignments because the thought of starting them is overwhelming. Feel irritable and exhausted all the time. Need a reset button."
  },
  {
    "entry_text": "Was told again today that my feelings aren't valid. That I shouldn't be upset. Starting to feel numb."
  },
  {
    "entry_text": "Spent the afternoon planning out my garden. Decided where the tomatoes and peppers will go, need to get some more compost. Also looked up companion planting guides – apparently basil is good near tomatoes? Need to figure out the watering schedule too, especially with the heat starting. Maybe I'll try zucchini again this year, even though I always end up with way too much. It felt good to be outside thinking about something productive."
  },
  {
    "entry_text": "Thinking about how I basically raised my younger siblings because Mom was always working or out. Made their lunches, got them ready for school, helped with homework. I missed out on a lot of kid stuff myself. Felt like I had to be the adult when I was just 10."
  },
  {
    "entry_text": "Got another unsolicited explicit picture in my DMs. Blocked them but feel grossed out and kind of violated. Why do guys do that?"
  },
  {
    "entry_text": "We had another fight, and he said if I ever tried to leave him, he'd make sure I regretted it. He didn't say how, just that 'I wouldn't like it.' It wasn't a physical threat exactly, but it felt like one. It makes leaving feel impossible."
  }
]


async def main():
    for entry in entries:
        user = await database.create_user()
        entry_id = await database.create_journal_entry(user)
        await database.update_journal_entry(entry_id=entry_id, note=entry["entry_text"], shared=True)
        classification = await gemini.classify(entry["entry_text"])
        print(entry["entry_text"])
        print(classification.category)
        await database.update_journal_entry(entry_id=entry_id, classification=classification.category)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
