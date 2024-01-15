./run.sh \
    --stage 6 \
    --tts_task gan_tts \
    --train_args "--batch_size 8" \
    --train_config ./conf/tuning/train_joint_conformer_fastspeech2_hifigan.yaml \
    --teacher_dumpdir exp/tts_train_raw_phn_tacotron_g2p_en_no_space/decode_use_teacher_forcingtrue_train.loss.best 
