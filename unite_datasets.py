import os


def unite_datasets(dataset_dir1, dataset_dir2, output_dir):
    #check if output_dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #create train, test valid dirs inside output_dir
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    valid_dir = os.path.join(output_dir, 'valid')
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)

    #move all dirs from dirs tranin, test and valid inside dataset_dir1 and dataset_dir2 to output_dir
    for dir in os.listdir(dataset_dir1):
        if os.path.isdir(os.path.join(dataset_dir1, dir)) and dir in ['train', 'test', 'valid']:
            #copy all dirs from dir to output_dir
            for subdir in os.listdir(os.path.join(dataset_dir1, dir)):
                os.mkdir(os.path.join(output_dir, dir, subdir))
                for file in os.listdir(os.path.join(dataset_dir1, dir, subdir)):
                    os.rename(os.path.join(dataset_dir1, dir, subdir, file), os.path.join(output_dir, dir, subdir, file))
            
    for dir in os.listdir(dataset_dir2):
        if os.path.isdir(os.path.join(dataset_dir2, dir)) and dir in ['train', 'test', 'valid']:
            #copy all dirs from dir to output_dir
            for subdir in os.listdir(os.path.join(dataset_dir2, dir)):
                os.mkdir(os.path.join(output_dir, dir, subdir))
                for file in os.listdir(os.path.join(dataset_dir2, dir, subdir)):
                    os.rename(os.path.join(dataset_dir2, dir, subdir, file), os.path.join(output_dir, dir, subdir, file))
