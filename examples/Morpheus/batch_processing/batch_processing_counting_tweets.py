from Morpheus.data_loading import get_files_list, read_compressed_bz2_json_file
from Morpheus.batch_processing import process_in_batches_generator, process_in_batches


def counter(tweets):
    return len(tweets)


def example_process_in_batches():
    """
    Example function to show how process_in_batches works
    :return: returns the count of tweets
    """
    files_lst = get_files_list('../../../data/*.json.bz2')
    results = process_in_batches(files_lst, read_func=read_compressed_bz2_json_file, func_to_apply=counter,
                                 verbose=False)
    return results


def example_process_in_batches_generator():
    """
    Example function to show how process_in_batches_generator works
    :return: returns the count of tweets
    """

    files_lst = get_files_list('../../../data/*.json.bz2')
    generator = process_in_batches_generator(files_lst, read_func=read_compressed_bz2_json_file, func_to_apply=counter)
    results = list(generator)
    return results


if __name__ == "__main__":
    print()
    print("Output from process_in_batches:", example_process_in_batches())
    print("Output from process_in_batches_generator:", example_process_in_batches_generator())
    print()
