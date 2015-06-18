__author__ = 'jjb'


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



# 1) Load preanalysed features from csv: pre_features

# set feature type
feature_type = 'rp' # rhythmic: rp, rh   more timbral: ssd
feature_sets = [feature_type] # this usually is an array of multiple feature sets
filenamestub = 'features'

# our ids are the original mp3_filenames
mp3_filenames, db_features = read_feature_files(filenamestub,feature_sets)





# 2) analyze new track

audiofile = "./generated.wav"


audiofile = "./generated.wav"

audiofile = "/Users/jjb/Music/mp3/1972/1972-095 Detroit Emeralds - Baby Let Me Take You (In My Arms).mp3"

samplerate, samplewidth, wavedata = audiofile_read(audiofile)

# adapt the fext array to your needs:
# fext = ['rp','ssd','rh'] # ,'mvd' sh, tssd, trh
fext = feature_sets

query_features = rp_extract(wavedata,
                  samplerate,
                  extract_rp   = ('rp' in fext),          # extract Rhythm Patterns features
                  extract_ssd  = ('ssd' in fext),           # extract Statistical Spectrum Descriptor
                  extract_sh   = ('sh' in fext),          # extract Statistical Histograms
                  extract_tssd = ('tssd' in fext),          # extract temporal Statistical Spectrum Descriptor
                  extract_rh   = ('rh' in fext),           # extract Rhythm Histogram features
                  extract_trh  = ('trh' in fext),          # extract temporal Rhythm Histogram features
                  extract_mvd  = ('mvd' in fext),        # extract Modulation Frequency Variance Descriptor
                  spectral_masking=True,
                  transform_db=True,
                  transform_phon=True,
                  transform_sone=True,
                  fluctuation_strength_weighting=True,
                  skip_leadin_fadeout=0,
                  step_width=1)




# 3) search for similar songs

# we decided for one feature type above

query_feature_vector = query_features[feature_type]

db_feature_vectors = db_features[feature_type]

# Initialize the similarity search object

sim_song_search = NearestNeighbors(n_neighbors = 6, metric='euclidean')

# TODO proper Scaling (Normalization) would need to add the live extracted song to the db_features

# Normalize the extracted features
# scaled_feature_space = StandardScaler().fit_transform(demoset_features)

# Fit the Nearest-Neighbor search object to the extracted features
# sim_song_search.fit(scaled_feature_space)

sim_song_search.fit(db_feature_vectors)


(distances, similar_song_ids) = sim_song_search.kneighbors(query_feature_vector, return_distance=True)


# because we are searching in the entire collection, the top-most result is the query song itself. Thus, we can skip it.
# just if the query is in the feature set (if normalisation is used)
#similar_songs = similar_songs[1:]

print similar_song_ids

print "Most similar files:"

print mp3_filenames[feature_type][similar_song_ids]