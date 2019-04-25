python test.py --name xl_landscape-0422 \
                --dataset_mode custom \
                --label_dir datasets/xueluo_landscope/val_label/ \
                --image_dir datasets/xueluo_landscope/val_img/ \
                --instance_dir datasets/xueluo_landscope/val_instance/ \
                --gpu_ids -1 \
                --label_nc 182 \
                --no_instance \
                --crop_size 512 \
                --load_size 512 \

