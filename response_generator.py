"""
Developed by py.mongo
"""

import json
import random
import datetime
import locale
import pymongo
import uuid

import intent_classifier

ticket_count = 50
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SidoChatbotId"]
destination_collection = db["wisata"]
feedback_collection = db["tanggapan"]
tickets_collection = db["tiket"]
with open("dataset.json") as file:
    data = json.load(file)


def get_intent(message):
    tag = intent_classifier.classify(message)
    return tag


"""
Reduce seat_count variable by 1
Generate and give customer a unique booking ID if tickets available
Write the booking_id and time of booking into Collection named bookings in restaurant database
"""


def book_ticket():
    global ticket_count  # dapat diakses seluruh program
    ticket_count -= 1
    ticket_id = str(uuid.uuid4())
    now = datetime.datetime.now()
    ticket_time = now.strftime("%Y-%m-%d %H:%M:%S")
    ticket_doc = {"id_tiket": ticket_id, "waktu_pesan": ticket_time}
    tickets_collection.insert_one(ticket_doc)
    return ticket_id


def tourist_list():
    query = {"wisata": "Y"}
    destination_doc = destination_collection.find(query)
    if destination_doc.count() > 0:
        response = "Wisata pilihan: "
        for x in destination_doc:
            response = (
                response
                + str(x.get("tempat"))
                + " untuk Rp. "
                + str(x.get("biaya"))
                + "; "
            )
        response = response[:-2]  # to remove the last ;
    else:
        response = "Maaf wisata tidak tersedia"
    return response


def traveler_list():
    query = {"traveler": "Y"}
    query = {"wisata": "Y"}
    destination_doc = destination_collection.find(query)
    if destination_doc.count() > 0:
        response = "Wisata pilihan: "
        for x in destination_doc:
            response = (
                response
                + str(x.get("tempat"))
                + " untuk Rp. "
                + str(x.get("biaya"))
                + "; "
            )
        response = response[:-2]  # to remove the last ;
    else:
        response = "Maaf wisata tidak tersedia"
    return response


def offers():
    all_offers = destination_collection.distinct("penawaran")
    if len(all_offers) > 0:
        response = "Penawaran spesial:  "
        for ofr in all_offers:
            docs = destination_collection.find({"penawaran": ofr})
            response = response + " " + ofr.upper() + " On: "
            for x in docs:
                response = (
                    response
                    + str(x.get("tempat"))
                    + " - Rs. "
                    + str(x.get("biaya"))
                    + "; "
                )
            response = response[:-2]  # to remove the last ;
    else:
        response = "Maaf sedang tidak tersedia sekarang"
    return response


def suggest():
    locale.setlocale(locale.LC_TIME, "id_ID.utf8")
    day = datetime.datetime.now()
    day = day.strftime("%A")
    if day == "Senin":
        response = "Rekomendasi destinasi terbaik kami untuk hari ini adalah Gunung Kelud. Menawarkan pemandangan yang menakjubkan dan kesempatan untuk menjelajahi alam pada titik terbaiknya."
    elif day == "Selasa":
        response = "Hari ini, kami menyarankan mengunjungi Gereja Puh Sarang. Ini adalah keajaiban arsitektur unik yang diukir di dalam gua perbukitan, menawarkan suasana yang tenang."

    elif day == "Rabu":
        response = "Untuk petualangan hari ini, kami merekomendasikan menjelajahi Air Terjun Jagir yang indah. Ini adalah tempat yang menyegarkan bagi pecinta alam dan fotografer."

    elif day == "Kamis":
        response = "Rekomendasi kami untuk hari ini adalah mengunjungi Museum Kerajaan Kediri yang bersejarah. Selami sejarah dan budaya Kediri yang kaya."

    elif day == "Jumat":
        response = "Mengapa tidak menghabiskan hari ini menjelajahi Air Terjun Nglirip yang mempesona? Ini adalah permata tersembunyi dengan air yang jernih dan lingkungan yang subur."

    elif day == "Sabtu":
        response = "Hari ini, kami menyarankan perjalanan ke dataran tinggi Puhsarang yang megah. Nikmati pemandangan panorama Kediri dan tenggelamkan diri Anda dalam ketenangannya."

    elif day == "Minggu":
        response = "Rekomendasi utama kami untuk hari ini adalah mengunjungi ikon Simpang Lima Gumul. Ini adalah alun-alun yang ramai dengan energi yang semarak dan pesona lokal."
    return response


def intinerary_enquiry(message):
    all_destinations = destination_collection.distinct("tempat")
    response = ""
    for destiny in all_destinations:
        query = {"tempat": destiny}
        destination_doc = destination_collection.find(query)[0]
        if destiny.lower() in message.lower():
            response = destination_doc.get("tentang")
            break
    if "" == response:
        response = (
            "Maaf, silakan coba lagi dengan ejaan yang tepat dari wisata yang tersedia!"
        )
    return response


def record_feedback(message, type):
    feedback_doc = {"tanggapan_string": message, "tipe": type}
    feedback_collection.insert_one(feedback_doc)


def get_specific_response(tag):
    for intent in data["intents"]:
        if intent["tag"] == tag:
            responses = intent["responses"]
    response = random.choice(responses)
    return response


def show_destination():
    all_items = destination_collection.distinct("tempat")
    response = ", ".join(all_items)
    return response


def generate_response(message):
    global ticket_count
    tag = get_intent(message)
    print(f"Intent detected: {tag}")  # debbuging
    response = ""
    if tag != "":
        if tag == "pesan_tiket":

            if ticket_count > 0:
                ticket_id = book_ticket()
                response = "Pemesanan tiket sukses" + str(ticket_id)
            else:
                response = "Maaf saat ini sedang sold out!"

        elif tag == "tiket_tersedia":
            response = (
                "There are "
                + str(ticket_count)
                + " visitor(s) available at the moment."
            )

        elif tag == "traveler_tanya":
            response = traveler_list()

        elif tag == "turis_tanya":
            response = tourist_list()

        elif tag == "offers":
            response = offers()

        elif tag == "suggest":
            response = suggest()

        elif tag == "intinerary_enquiry":
            response = intinerary_enquiry(message)

        elif tag == "destination":
            response = show_destination()

        elif tag == "positive_feedback":
            record_feedback(message, "positive")
            response = "Thank you so much for your valuable feedback. We look forward to serving you again!"

        elif tag == "negative_feedback":
            record_feedback(message, "negative")
            response = (
                "Thank you so much for your valuable feedback. We deeply regret the inconvenience. We have "
                "forwarded your concerns to the authority and hope to satisfy you better the next time! "
            )
        # for other intents with pre-defined responses that can be pulled from dataset
        else:
            response = get_specific_response(tag)
    else:
        response = "Sorry! I didn't get it, please try to be more precise."
        print(f"Response: {response}")  # debbuging
    return response
