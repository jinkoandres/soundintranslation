__author__ = 'jjb'


# Rhythm Pattern Audio Extraction Library
## edit the path here where you checked out and stored the rp_extract package
import sys
sys.path.append("./rp_extract")

from rp_plot import *
from rp_extract_python import rp_extract


# for Similarity Search import
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Initialize the similarity search object

sim_song_search = NearestNeighbors(n_neighbors = 6, metric='euclidean')

# set feature type
feature_set = 'rh'

# TODO: Load preanalysed features from csv: pre_features

# Normalize the extracted features
# scaled_feature_space = StandardScaler().fit_transform(demoset_features)

# Fit the Nearest-Neighbor search object to the extracted features
# sim_song_search.fit(scaled_feature_space)

sim_song_search.fit(pre_features)



# 1) analyze new track

audiofile = "./generated.wav"

samplerate, samplewidth, wavedata = audiofile_read(audiofile)

# adapt the fext array to your needs:
fext = ['rp','ssd','rh'] # ,'mvd' sh, tssd, trh

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

(distances, similar_songs) = sim_song_search.kneighbors(query_track_feature_vector, return_distance=True)


# because we are searching in the entire collection, the top-most result is the query song itself. Thus, we can skip it.
# just if the query is in the feature set (if normalisation is used)
#similar_songs = similar_songs[1:]



