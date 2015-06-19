__author__ = 'jjb'

# support / additional author: Thomas Lidy


# Rhythm Pattern Audio Extraction Library
## edit the path here where you checked out and stored the rp_extract package
import sys
sys.path.append("../rp_extract")
# reading wav and mp3 files
from audiofile_read import *  # included in the rp_extract git package
from rp_extract_files import read_feature_files
from rp_extract_python import rp_extract

# for Similarity Search import
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors



# IMPORTANT:
# we define query_features as global variable
# as we need to reuse them in BOTH functions below
# only getSimilarSongs will set (write) it, getSimilarSongSegments will read it only

query_features = {}


# getSimilarSongs:

# audiofile: name of .wav (or .mp3) file to be analyzed as new query
# reference_db_filenames: list of audio filenames that were pre-analyzed
# reference_db_features: a dict containing the pre-analyzed features from the reference_db
# feature_type: feature type to be used for similarity search: 'rh' or 'rp' or 'ssd' ...

def getSimilarSongs(audiofile, reference_db_filenames, reference_db_features, feature_type = 'rh'):

    global query_features # GLOBAL VAR because it is reused in getSimilarSongSegments (see IMPORTANT note above)

    # Read Wav File

    samplerate, samplewidth, wavedata = audiofile_read(audiofile)

    # Analyze New Audio

    # here we set the feature type for the analysis, but we need to put it in a list [.]
    fext = [feature_type]

    query_features = rp_extract(wavedata,
                      samplerate,
                      extract_rp   = ('rp' in fext),          # extract Rhythm Patterns features
                      extract_ssd  = ('ssd' in fext),           # extract Statistical Spectrum Descriptor
                      extract_sh   = ('sh' in fext),          # extract Statistical Histograms
                      extract_tssd = ('tssd' in fext),          # extract temporal Statistical Spectrum Descriptor
                      extract_rh   = ('rh' in fext),           # extract Rhythm Histogram features
                      extract_trh  = ('trh' in fext),          # extract temporal Rhythm Histogram features
                      extract_mvd  = ('mvd' in fext),        # extract Modulation Frequency Variance Descriptor
                      skip_leadin_fadeout=0,
                      step_width=1)

    # from the dict returned by rp_extract, we take only the one feature_type we want
    query_feature_vector = query_features[feature_type]

    # reference_db_features should be a dict containing several feature types
    # we take the feature type given as parameter

    reference_feature_vectors = reference_db_features[feature_type]

    # Search for similar songs in pre-analyzed song dataset (based on song's averaged features)

    # initialize the similarity search object
    sim_song_search = NearestNeighbors(n_neighbors = 6, metric='euclidean')

    # TODO proper Scaling (Normalization) would need to add the live extracted song to the db_features

    # Normalize the extracted features
    # scaled_feature_space = StandardScaler().fit_transform(reference_feature_vectors)

    # Fit the Nearest-Neighbor search object to the scaled features
    # sim_song_search.fit(scaled_feature_space)

    sim_song_search.fit(reference_feature_vectors)

    # Get the most similar songs
    (distances, similar_song_ids) = sim_song_search.kneighbors(query_feature_vector, return_distance=True)

    # if the query is contained in the db feature set (usually if normalisation is used) we need to take it away from the result
    #similar_songs = similar_songs[1:]

    #print similar_song_ids

    most_similar_songs = reference_db_filenames[feature_type][similar_song_ids]

    # most_similar_songs is a 2D np.array, make it 1D
    most_similar_songs = most_similar_songs[0]

    # transform from np.array to simple list
    most_similar_songs = most_similar_songs.tolist()

    return(most_similar_songs)



# getSimilarSongSegments:

# YOU MUST CALL getSimilarSongs BEFORE!

# audiofile: name of .wav (or .mp3) file to be analyzed as new query
# feature_type: feature type to be used for similarity search: 'rh' or 'rp' or 'ssd' ...

def getSimilarSongSegments(audiofile, feature_type = 'rh'):

    samplerate, samplewidth, wavedata = audiofile_read(audiofile)

    # here we set the feature type for the analysis, but we need to put it in a list [.]
    fext = [feature_type]

    segment_features = rp_extract(wavedata,
                      samplerate,
                      extract_rp   = ('rp' in fext),          # extract Rhythm Patterns features
                      extract_ssd  = ('ssd' in fext),           # extract Statistical Spectrum Descriptor
                      extract_sh   = ('sh' in fext),          # extract Statistical Histograms
                      extract_tssd = ('tssd' in fext),          # extract temporal Statistical Spectrum Descriptor
                      extract_rh   = ('rh' in fext),           # extract Rhythm Histogram features
                      extract_trh  = ('trh' in fext),          # extract temporal Rhythm Histogram features
                      extract_mvd  = ('mvd' in fext),        # extract Modulation Frequency Variance Descriptor
                      skip_leadin_fadeout=0,
                      step_width=1,
                      return_segment_features = True)

    search_features = segment_features[feature_type]

    # IMPORTANT: we use query_features as a GLOBAL VARIABLE here
    # that means getSimilarSongs MUST ALWAYS BE CALLED BEFORE THIS FUNCTION
    query_feature_vector = query_features[feature_type]

    # Searching similar song segments

    sim_song_search = NearestNeighbors(n_neighbors = 1, metric='euclidean')

    # TODO proper Scaling (Normalization) (see above)

    sim_song_search.fit(search_features)

    # Get the most similar song SEGMENTS indices
    most_similar_segment_index = sim_song_search.kneighbors(query_feature_vector, return_distance=False)

    # here you get the segment's sample position
    # segment_features['segpos']

    # and time positions in seconds
    # segment_features['timepos']

    # print most_similar_segment_index

    # print segment_features['segpos'][most_similar_segment_index]

    most_similar_timestamp = segment_features['timepos'][most_similar_segment_index]

    # print most_similar_timestamp

    # quit the [[[]]] (we got a nested array for some reason)
    most_similar_timestamp = most_similar_timestamp[0][0]

    # print most_similar_timestamp

    # return tuple (start_pos, end_pos)
    return (most_similar_timestamp[0],most_similar_timestamp[1])


# defGetCenteredSegment(...):
# THIS IS TEST CODE, NOT YET FINISHED
    # 5) get 30 seconds around the middle timestamp

    # output_length = 30 # duration of desired output segment in seconds
    #
    # middle_timestamp = (most_similar_timestamp[0] + most_similar_timestamp[1]) / 2
    #
    # print middle_timestamp
    #
    # start_pos = middle_timestamp - (output_length / 2)
    # if start_pos < 0:
    #     start_pos = 0
    #
    # end_pos = start_pos + output_length
    # # TODO:
    # # if end_pos > duration of song
    #     # end pos = duration of song
    #     # start_pos = end_pos - output_length
    # # TODO: MAYBE ITS BETTER to do everything in samples (segpos) instead of timepos
    #
    # print "Output segment:", start_pos, end_pos




if __name__ == '__main__':


    # REFERENCE DATA SET

    # 0) We pre-analyzed a set of MP3 files to store the features in a CSV file

    # using rp_extract_files.py
    # editing the in_path and out_path in the __main__ function

    # set the same path here as used in rp_extract_files.py
    MP3_PATH = "/Users/jjb/Music/mp3/1972/"


    # 1) Load pre-analysed features from csv: pre_features

    # set feature type
    feature_type = 'rh' # rhythmic: rp, rh   more timbral: ssd

    feature_sets = [feature_type] # here we set the same, but this usually is an array of multiple feature sets [.]

    filenamestub = 'features'

    # read CSV: get the ids and features
    # our ids are the mp3_filenames (relative path only)
    mp3_filenames, reference_db_filenames = read_feature_files(filenamestub,feature_sets)

    # get similar songs with new wav file:

    new_wavfile = "./generated.wav"

    similar_songs = getSimilarSongs(new_wavfile, mp3_filenames, reference_db_filenames, feature_type)

    print "Most similar songs:"

    for song in similar_songs:
        print song

    # Which song (0, 1, 2 ...) do you want to get the best segments from (max. 5)

    song_n = 0

    audiofile = MP3_PATH + similar_songs[song_n]

    print audiofile

    # FIND THE BEST SEGMENT that matches the original query

    (start_time, end_time) = getSimilarSongSegments(audiofile, feature_type)

    print start_time, end_time

