ALBERT_BASE_DIR=../ALBERT/model
DATA_DIR=../../dat/Analgesics-induced_acute_liver_failure/
OUTPUT_DIR=../../dat/Analgesics-induced_acute_liver_failure/output/
python ../ALBERT/run_classifier.py \
    --data_dir=$DATA_DIR \
    --output_dir=$OUTPUT_DIR \
    --init_checkpoint=$ALBERT_BASE_DIR/model.ckpt-best \
    --albert_config_file=$ALBERT_BASE_DIR/albert_config.json \
    --vocab_file=$ALBERT_BASE_DIR/30k-clean.vocab \
    --spm_model_file=$ALBERT_BASE_DIR/30k-clean.model \
    --do_train \
    --do_eval \
    --do_predict \
    --do_lower_case \
    --max_seq_length=128 \
    --optimizer=adamw \
    --task_name=causal \
    --warmup_step=200 \
    --learning_rate=2e-5 \
    --train_step=30000 \
    --save_checkpoints_steps=3000 \
    --train_batch_size=32
