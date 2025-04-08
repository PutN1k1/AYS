from TTS.api import TTS
from pydub import AudioSegment


def generate_voiceover(text, output_path, slowed_output_path=None, slow_factor=0.95):

    print("Генерация озвучки...")
    tts = TTS("tts_models/en/vctk/vits").to("cpu")
    tts.tts_to_file(text=text, file_path=output_path, speaker="p251")

    if slowed_output_path:
        print("🐢 Замедление аудио...")
        audio = AudioSegment.from_wav(output_path)
        slowed_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * slow_factor)
        }).set_frame_rate(audio.frame_rate)
        slowed_audio.export(slowed_output_path, format="wav")
        print(f"Замедленная озвучка сохранена: {slowed_output_path}")
    else:
        print(f"Озвучка создана: {output_path}")


if __name__ == "__main__":
    text = (
        "Atomic bombs are among humanity’s most devastating inventions. Developed during World War II under the "
        "Manhattan Project, these weapons harness nuclear fission—splitting heavy atoms like uranium or "
        "plutonium—to unleash immense energy. The first atomic bomb was detonated in 1945, and shortly after, "
        "two were dropped on Hiroshima and Nagasaki, killing over 200,000 people and ending the war, but sparking "
        "global ethical debates. A single atomic bomb can destroy entire cities, generate firestorms, "
        "and leave lasting radiation, causing cancer and genetic damage. Modern thermonuclear weapons (hydrogen "
        "bombs) use fusion, making them thousands of times more powerful. The Cold War saw a terrifying arms race, "
        "with nations stockpiling nukes under the doctrine of “mutually assured destruction.” Today, "
        "nine countries possess roughly 12,500 nuclear warheads. While treaties aim to limit proliferation, "
        "risks of accidents, terrorism, or conflict remain. Atomic bombs symbolize humanity’s capacity for both "
        "scientific achievement and existential danger. Their existence compels us to confront a critical "
        "question: Will we wield this power responsibly, or face catastrophic consequences?"
    )

    original_output = "voice.wav"
    slowed_output = "voice_slowed.wav"

    generate_voiceover(text, original_output, slowed_output_path=slowed_output)
