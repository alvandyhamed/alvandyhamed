from pathlib import Path
import re,json,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
for path in (root/'assets').glob('*.svg'):
    tree=ET.parse(path)
    for node in tree.iter():
        assert node.tag.split('}')[-1] not in {'script','foreignObject'},path
        assert not any(k.lower().startswith('on') for k in node.attrib),path
        assert not any(k.endswith('href') and not v.startswith('#') for k,v in node.attrib.items()),path
for path in re.findall(r'(?:src|srcset)="([^"]+)"',(root/'README.md').read_text()):
    assert (root/path).is_file(),path
stats=json.loads((root/'assets/stats.json').read_text())
for key in ['total_repositories','public_repositories','private_repositories','contributions_last_year']:
    assert type(stats[key]) is int and stats[key]>=0
for theme in ['dark','light']:
    text=(root/f'assets/stats-{theme}.svg').read_text()
    assert stats['as_of'] in text
    for key in ['total_repositories','public_repositories','private_repositories','contributions_last_year']:
        assert f'>{stats[key]}</text>' in text
assert 'DRAFT PROFILE' in (root/'README.md').read_text()
print('PASS: SVG safety, local README images, dated statistics and draft label')

assert stats['total_repositories'] == stats['public_repositories'] + stats['private_repositories']
