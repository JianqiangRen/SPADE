python train.py --name xl_landscape-0422  \
                --dataset_mode custom \
                --label_dir ../deeplab-pytorch/landscape_dataset/landscape_train_label/  \
                --image_dir ../deeplab-pytorch/landscape_dataset/landscape_train_img/  \
                --label_nc 182 \
                --no_instance \
                --niter 300 \
                --tf_log