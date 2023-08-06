"""Test common skift functionalities."""

import pytest
import pandas as pd
from sklearn.model_selection import cross_val_score

from skift import (
    FirstColFtClassifier,
    IdxBasedFtClassifier,
    ColLblBasedFtClassifier,
    FirstObjFtClassifier,
)


def _ftdf():
    return pd.DataFrame(
        data=[['woof woof', 0], ['meow meow', 1]],
        columns=['txt', 'lbl']
    )


def test_bad_shape():
    ft_clf = FirstColFtClassifier()
    with pytest.raises(ValueError):
        ft_clf.fit([7], [0])
    with pytest.raises(ValueError):
        ft_clf.fit([[7]], [[0]])


def test_predict():
    ftdf = _ftdf()
    ft_clf = FirstColFtClassifier()
    ft_clf.fit(ftdf[['txt']], ftdf['lbl'])

    assert ft_clf.predict([['woof woof']])[0] == 0
    assert ft_clf.predict([['meow meow']])[0] == 1
    assert ft_clf.predict([['meow']])[0] == 1
    assert ft_clf.predict([['woof lol']])[0] == 0
    assert ft_clf.predict([['meow lolz']])[0] == 1


def test_predict_proba():
    ftdf = _ftdf()
    ft_clf = FirstColFtClassifier()
    ft_clf.fit(ftdf[['txt']], ftdf['lbl'])

    res = ft_clf.predict_proba([['woof woof']])[0]
    assert res[0] > res[1]
    res = ft_clf.predict_proba([['meow meow']])[0]
    assert res[1] > res[0]


def test_idx_based():
    ftdf = _ftdf()
    ft_clf = IdxBasedFtClassifier(0)
    ft_clf.fit(ftdf[['txt']], ftdf['lbl'])

    assert ft_clf.predict([['woof woof']])[0] == 0
    assert ft_clf.predict([['meow meow']])[0] == 1
    assert ft_clf.predict([['meow']])[0] == 1
    assert ft_clf.predict([['woof lol']])[0] == 0
    assert ft_clf.predict([['meow lolz']])[0] == 1


def test_first_obj():
    ftdf = _ftdf()
    ft_clf = FirstObjFtClassifier()
    ft_clf.fit(ftdf[['txt']], ftdf['lbl'])

    assert ft_clf.predict(pd.DataFrame([['woof woof']]))[0] == 0
    assert ft_clf.predict(pd.DataFrame([['meow meow']]))[0] == 1
    assert ft_clf.predict(pd.DataFrame([['meow']]))[0] == 1
    assert ft_clf.predict(pd.DataFrame([['woof lol']]))[0] == 0
    assert ft_clf.predict(pd.DataFrame([['meow lolz']]))[0] == 1

    with pytest.raises(ValueError):
        assert ft_clf.predict(pd.DataFrame([[5]]))[0] == 1


def test_col_lbl():
    ftdf = _ftdf()
    ft_clf = ColLblBasedFtClassifier('txt', epoch=14)
    ft_clf.fit(ftdf[['txt']], ftdf['lbl'])

    assert ft_clf.predict(pd.DataFrame(
        [['woof woof']], columns=['txt']))[0] == 0
    assert ft_clf.predict(
        pd.DataFrame([['meow meow']], columns=['txt']))[0] == 1
    assert ft_clf.predict(
        pd.DataFrame([['meow']], columns=['txt']))[0] == 1
    assert ft_clf.predict(
        pd.DataFrame([['woof lol']], columns=['txt']))[0] == 0
    assert ft_clf.predict(
        pd.DataFrame([['meow lolz']], columns=['txt']))[0] == 1


def test_bad_param():
    ftdf = _ftdf()
    ft_clf = ColLblBasedFtClassifier('txt', bad_param=14)
    with pytest.raises(TypeError):
        ft_clf.fit(ftdf[['txt']], ftdf['lbl'])


def _big_ftdf():
    return pd.DataFrame(
        data=[
            ['woof woof', 0],
            ['woof', 0],
            ['howl', 0],
            ['growl', 0],
            ['meow meow', 1],
            ['meow', 1],
            ['prr', 1],
            ['cheezburger', 1],
        ],
        columns=['txt', 'lbl']
    )


def test_cross_val():
    ft_clf = ColLblBasedFtClassifier('txt', epoch=3)
    ftdf = _big_ftdf()
    cross_val_score(
        ft_clf, X=ftdf[['txt']], y=ftdf['lbl'], cv=2, scoring='accuracy')

    ft_clf = IdxBasedFtClassifier(0, epoch=3)
    ftdf = _big_ftdf()
    cross_val_score(
        ft_clf, X=ftdf[['txt']], y=ftdf['lbl'], cv=2, scoring='accuracy')

    ft_clf = FirstColFtClassifier(epoch=3)
    ftdf = _big_ftdf()
    cross_val_score(
        ft_clf, X=ftdf[['txt']], y=ftdf['lbl'], cv=2, scoring='accuracy')
