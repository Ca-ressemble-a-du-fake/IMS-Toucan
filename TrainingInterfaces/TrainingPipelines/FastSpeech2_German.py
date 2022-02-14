import random

import torch
from torch.utils.data import ConcatDataset

from TrainingInterfaces.Text_to_Spectrogram.FastSpeech2.FastSpeech2 import FastSpeech2
from TrainingInterfaces.Text_to_Spectrogram.FastSpeech2.fastspeech2_train_loop import train_loop
from Utility.corpus_preparation import prepare_fastspeech_corpus
from Utility.path_to_transcript_dicts import *


def run(gpu_id, resume_checkpoint, finetune, model_dir, resume):
    if gpu_id == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        device = torch.device("cpu")

    else:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(gpu_id)
        device = torch.device("cuda")

    torch.manual_seed(131714)
    random.seed(131714)
    torch.random.manual_seed(131714)

    print("Preparing")

    if model_dir is not None:
        save_dir = model_dir
    else:
        save_dir = os.path.join("Models", "FastSpeech2_German")
    os.makedirs(save_dir, exist_ok=True)

    datasets = list()
    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_karlsson(),
                                              corpus_dir=os.path.join("Corpora", "Karlsson"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_eva(),
                                              corpus_dir=os.path.join("Corpora", "Eva"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_hokus(),
                                              corpus_dir=os.path.join("Corpora", "Hokus"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_bernd(),
                                              corpus_dir=os.path.join("Corpora", "Bernd"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_friedrich(),
                                              corpus_dir=os.path.join("Corpora", "Friedrich"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_hui_others(),
                                              corpus_dir=os.path.join("Corpora", "hui_others"),
                                              lang="de"))

    datasets.append(prepare_fastspeech_corpus(transcript_dict=build_path_to_transcript_dict_thorsten(),
                                              corpus_dir=os.path.join("Corpora", "Thorsten"),
                                              lang="de"))

    train_set = ConcatDataset(datasets)

    model = FastSpeech2(lang_embs=100)

    print("Training model")
    train_loop(net=model,
               train_dataset=train_set,
               device=device,
               save_directory=save_dir,
               steps=500000,
               batch_size=32,
               lang="de",
               lr=0.0001,
               warmup_steps=14000,
               path_to_checkpoint=resume_checkpoint,
               fine_tune=finetune,
               resume=resume)
