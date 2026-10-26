import csv
from pathlib import Path

def create_rich_dataset():
    # Ensure data/raw directory exists
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / "train_lyrics.csv"

    print("🔄 Generating 300+ multilingual and multi-genre lyric samples...")

    # Base pools of emotional lyrics across Bulgarian, English, and Spanish
    joy_pool = [
        "Слънцето грее и днес съм толкова щастлив!",
        "Let's go, party all night, we have the energy and life!",
        "Estoy tan feliz hoy, todo es maravilloso y brillante.",
        "Усмихвам се на целия свят, защото всичко е перфектно.",
        "We're flying high, nothing can stop this joy inside!",
        "Празнуваме до сутринта, музиката свири силно за нас.",
        "Всички си ръкопляскат, животът е прекрасен момент.",
        "¡Qué alegría tan grande siento al verte sonreír!"
    ]
    
    sadness_pool = [
        "Чувствам се толкова сам и тъжен в тази студена нощ.",
        "Me siento muy triste y con el corazón completamente roto.",
        "Ти угаси светлината в моето сърце и си тръгна завинаги.",
        "Sянката ти още броди из стаята, а теб те няма.",
        "Tears are falling down like rain on a lonely window.",
        "Останаха само спомени и празни чаши на масата.",
        "Всичко е сиво, болката в гърдите ми не спира.",
        "Nadie sabe cuántas lágrimas guardo en silencio."
    ]

    hype_pool = [
        "Вдигаме ръце във въздуха, клубът гори от енергия!",
        "We are the champions, tonight we own the entire world!",
        "¡Esta fiesta está increíble, con mucha potencia y flow!",
        "Газ до дупка, излизаме на улицата да мачкаме!",
        "Bass is pumping loud, everybody jump around now!",
        "Никой не може да ни спре тази вечер, летим нагоре!",
        "Adrenaline is rushing through my veins, let's go!"
    ]

    anger_pool = [
        "Всичко ме дразни, омръзна ми от тези фалшиви лъжи!",
        "Искам да крещя от яд заради цялото лицемерие тук!",
        "Няма да ти простя за това долно предателство!",
        "Me da tanta rabia ver cómo arruinas todo.",
        "You broke every rule, now face my fierce anger!",
        "Омразата ви ме гори, но само ме прави по-силен.",
        "Enough of your games, I'm burning this down!"
    ]

    nostalgia_pool = [
        "Спомням си старите дни, безгрижното ни детство...",
        "Колко бързо мина времето, къде останаха тези хубави дни?",
        "Los viejos tiempos regresan a mi mente como una película.",
        "Миризмата на лято и стари касети в колата...",
        "We were younger, wilder, and the world was ours.",
        "Връщам се назад в спомените, където всичко беше истинско.",
        "Aún recuerdo tu voz cantando bajo la lluvia de agosto."
    ]

    pools = [joy_pool, sadness_pool, hype_pool, anger_pool, nostalgia_pool]
    
    # Generate ~300 structured variations to build a solid training foundation
    data = []
    
    # We will loop and combine phrases to scale up to ~300 rows cleanly
    import random
    random.seed(42)

    target_rows = 300
    row_count = 0

    while row_count < target_rows:
        for label_idx, pool in enumerate(pools):
            base_text = random.choice(pool)
            # Add slight variations to make samples diverse
            variations = [
                f"{base_text}",
                f"Oh yeah, {base_text.lower()}",
                f"Знаеш как е: {base_text}",
                f"В тази песен се пее: {base_text}",
                f"Yeah, listen: {base_text}"
            ]
            text = random.choice(variations)
            data.append((text, label_idx))
            row_count += 1
            if row_count >= target_rows:
                break

    # Write to CSV in data/raw/
    with open(file_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(data)

    print(f"✅ Successfully created dataset with {len(data)} rows at: {file_path}")

if __name__ == "__main__":
    create_rich_dataset()