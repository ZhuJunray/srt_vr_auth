from ml4auth import knn_multi_kfolds, knn_multi, knn_binary, knn_binary_kfolds
from ml4auth import svm_multi_kfolds, svm_multi, svm_binary, svm_binary_kfolds
from dl4auth import mlp_multi_kfolds, mlp_binary_kfolds, mlp_binary, mlp_multi
import os, json, re, sys
from data_preprocess import data_augment_and_label, read_data_latter_data_json


################################################################ main
def main():
    os.chdir('D:\pycharm\srt_vr_auth')  # cwd的绝对路径
    positive_label = ['7']  # 正样本
    model = 'head'  # model
    n_split = 3  # k fold
    noise_level = 0.3  # noise level
    augmentation_time = 2  # 高斯噪声做数据增强的倍数
    size_list = [3]  # list of size
    pin_list = [14]  # pin list

    # 1.1update augment_time表示增强为原来数量的多少倍，如果留空则为默认值1，即全部为原始数据
    data_scaled, labels, binary_labels, scaled_data_augmented, binary_labels_augmented = data_augment_and_label(
        default_authentications_per_person=9, rotdir=os.path.join(os.getcwd(), "data/"), positive_label=positive_label,
        model=model, studytype_users_dates_range=read_data_latter_data_json()[0], size_list=size_list, pin_list=pin_list,
        noise_level=noise_level, augment_time=augmentation_time)

    print(f"labels:{labels}")
    print(f"binary_labels:{binary_labels}")
    print(f"binary_labels_augmented:{binary_labels_augmented}")
    print(f"data_scaled:{data_scaled.shape}")
    # print(f"scaler_origin:{scaler_origin.mean_}, scaler_augment:{scaler_augment.mean_}")
    # 原数据和标签跑机器学习模型
    print("")
    print("data augment for multiclass")

    # print("---------knn_binary_kfold------------")
    # knn_binary_kfolds(data_scaled=data_scaled, binary_labels=binary_labels,
    #                   n_splits=n_split)
    #
    # print("---------knn_multi_kfold------------")
    # knn_multi_kfolds(data_scaled=data_scaled, labels=labels,
    #                  n_splits=n_split)
    #
    # print("----------svm_binary_kfold------------")
    # svm_binary_kfolds(data_scaled=data_scaled, binary_labels=binary_labels,
    #                   n_splits=n_split)
    #
    # print("-----------svm_multi_kfold------------")
    # svm_multi_kfolds(data_scaled=data_scaled, labels=labels,
    #                  n_splits=n_split)

    print("------------mlp_binary_kfold------------")
    mlp_binary_kfolds(data_scaled=data_scaled, binary_labels=binary_labels,
                      n_splits=n_split)

    print("------------mlp_multi_kfold------------")
    mlp_multi_kfolds(data_scaled=data_scaled, labels=labels,
                     n_splits=n_split)

    # 数据增强后的数据和标签跑模型
    print("")
    print("data augment for binary")
    #
    # print("---------knn_binary_kfold------------")
    # knn_binary_kfolds(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
    #                   n_splits=n_split)
    #
    # print("----------svm_binary_kfold------------")
    # svm_binary_kfolds(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
    #                   n_splits=n_split)

    print("------------mlp_binary_kfold------------")
    mlp_binary_kfolds(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
                      n_splits=n_split)

    ################################ 随时间推移重新检验部分
    # 日后新采的数据属性
    default_latter_auth_per_person = 4  # 每人采集次数
    latter_positive_label = positive_label  # 正样本, 与之前是一致的

    latter_data_scaled, latter_labels, latter_binary_labels, _, _ = data_augment_and_label(
        default_authentications_per_person=default_latter_auth_per_person, rotdir=os.path.join(os.getcwd(), "data/"),
        positive_label=latter_positive_label, model=model,
        studytype_users_dates_range=read_data_latter_data_json()[1],
        size_list=size_list, pin_list=pin_list, noise_level=noise_level)

    print("")
    print(f"latter_data_scaled: {latter_data_scaled.shape}")
    print("")
    #
    # print("--------knn_binary------------")
    # knn_binary(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
    #            latter_data_scaled=latter_data_scaled, latter_labels=latter_binary_labels)
    #
    # print("---------knn_multi------------")
    # knn_multi(data_scaled=data_scaled, labels=labels, latter_data_scaled=latter_data_scaled,
    #           latter_labels=latter_labels)
    #
    # print("---------svm_binary------------")
    # svm_binary(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
    #            latter_data_scaled=latter_data_scaled, latter_labels=latter_binary_labels)
    #
    # print("---------svm_multi------------")
    # svm_multi(data_scaled=data_scaled, labels=labels,
    #           latter_data_scaled=latter_data_scaled, latter_labels=latter_labels)

    print("---------mlp_binary------------")
    mlp_binary(data_scaled=scaled_data_augmented, binary_labels=binary_labels_augmented,
               latter_data_scaled=latter_data_scaled, latter_labels=latter_binary_labels)

    print("-----------mlp_multi------------")
    mlp_multi(data_scaled=data_scaled, labels=labels,
              latter_data_scaled=latter_data_scaled, latter_labels=latter_labels)


if __name__ == "__main__":
    with open('output.txt', 'w') as file:  # 将print内容保存到文件
        # 保存当前的标准输出
        original_stdout = sys.stdout
        # 将标准输出重定向到文件
        sys.stdout = file
        main()
        # 恢复原来的标准输出
        sys.stdout = original_stdout

    # main() # 用于在终端输出print内容
