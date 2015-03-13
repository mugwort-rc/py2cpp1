#ifndef __TUPLE_PARSER_20150310__
#define __TUPLE_PARSER_20150310__

#include <string>

#include <boost/fusion/adapted.hpp>
#include <boost/fusion/include/adapt_struct.hpp>
#include <boost/spirit/include/qi.hpp>
#include <boost/spirit/include/phoenix.hpp>

struct node
{
  typedef std::shared_ptr<node> ptr;

  typedef enum {
    TEXT,
    TUPLE,
  } node_type;

  node(node_type type) :
    type(type)
  {}
  virtual ~node()
  {}

  node_type type;

};

struct text_node : node {
  text_node(const std::string &text) :
    node(TEXT),
    text(text)
  {}
  ~text_node()
  {}

  std::string text;

  static ptr create(const std::string &text)
  {
    return ptr(new text_node(text));
  }

};

typedef std::vector<node::ptr> node_list;

struct tuple_node : node {
  tuple_node(const node_list &nodes) :
    node(TUPLE),
    nodes(nodes)
  {}
  ~tuple_node()
  {}

  node_list nodes;

  static ptr create(const node_list &nodes)
  {
    return ptr(new tuple_node(nodes));
  }

};

template <typename Iterator, typename Skipper=boost::spirit::ascii::space_type>
struct tuple_grammar :
  boost::spirit::qi::grammar<Iterator, tuple_node::ptr(), Skipper>
{
  tuple_grammar() :
    tuple_grammar::base_type(tuple)
  {
    // tuple = '(' values ')'
    tuple = '('
          >> values [boost::spirit::_val=boost::phoenix::bind(
                       &tuple_node::create, boost::spirit::qi::_1)]
          >> ')'
          ;

    // values = value ',' (value (',' value)* ','?)?
    values = value >> ',' >> -(value % ',' >> -boost::spirit::qi::lit(','))
           ;

    // value = text | tuple
    value = text [boost::spirit::_val=boost::phoenix::bind(
                    &text_node::create, boost::spirit::qi::_1)]
          | tuple [boost::spirit::_val=boost::spirit::qi::_1]
          ;

    // text = text_char+
    text = boost::spirit::qi::lexeme[+text_char];

    // text_char = char - ',' - '(' - ')'
    text_char = boost::spirit::qi::char_ - ',' - '(' - ')';
  }

  boost::spirit::qi::rule<Iterator, std::string()>
    text_char, text;

  boost::spirit::qi::rule<Iterator, node::ptr(), Skipper>
    value;

  boost::spirit::qi::rule<Iterator, node_list(), Skipper>
    values;

  boost::spirit::qi::rule<Iterator, tuple_node::ptr(), Skipper>
    tuple;
};

tuple_node::ptr parse(const std::string &s)
{
  typedef std::string::const_iterator iterator_type;
  typedef tuple_grammar<iterator_type> Grammar;
  Grammar grammar;

  iterator_type iter = s.begin();
  iterator_type end = s.end();

  tuple_node::ptr result;
  bool r = boost::spirit::qi::phrase_parse(iter, end, grammar,
             boost::spirit::ascii::space, result);
  if ( ! r || iter != end ) {
    return tuple_node::ptr();
  }
  return result;
}

#endif
